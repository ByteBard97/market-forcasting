"""
Model Benchmark: Compare forecasting approaches on Air Jordan synthetic data.

Tests:
- Prophet (multiplicative)
- StatsForecast (AutoARIMA, AutoETS)
- XGBoost (with lag features)
- LightGBM (with lag features)
- Baseline (Naive, Seasonal Naive)

Evaluates on same test set with MAE, MAPE, RMSE, coverage.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Prophet
from prophet import Prophet

# StatsForecast
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive, Naive

# Gradient Boosting
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error


class ForecastBenchmark:
    """
    Benchmark multiple forecasting models on a single segment.
    """

    def __init__(
        self,
        segment_data: Dict,
        test_horizon: int = 7,  # Default: 1 week (was 8 weeks)
        forecast_freq: str = "D"
    ):
        """
        Initialize benchmark.

        Args:
            segment_data: Segment JSON data
            test_horizon: Number of periods to hold out for testing
            forecast_freq: Forecast frequency ('D' daily, 'W' weekly)
        """
        self.segment_data = segment_data
        self.test_horizon = test_horizon
        self.freq = forecast_freq

        # Prepare data
        self.df = pd.DataFrame({
            'ds': pd.to_datetime(segment_data['calendar']['ds']),
            'y': segment_data['observed']['units']
        })

        # Train/test split
        self.train_df = self.df.iloc[:-test_horizon].copy()
        self.test_df = self.df.iloc[-test_horizon:].copy()

        self.results = {}

    def _create_lag_features(self, df: pd.DataFrame, lags: List[int] = [1, 7, 14, 28]) -> pd.DataFrame:
        """Create lagged features for ML models."""
        df = df.copy()

        for lag in lags:
            df[f'lag_{lag}'] = df['y'].shift(lag)

        # Rolling statistics
        df['rolling_mean_7'] = df['y'].shift(1).rolling(window=7).mean()
        df['rolling_std_7'] = df['y'].shift(1).rolling(window=7).std()
        df['rolling_mean_28'] = df['y'].shift(1).rolling(window=28).mean()

        # Date features
        df['dayofweek'] = df['ds'].dt.dayofweek
        df['month'] = df['ds'].dt.month
        df['quarter'] = df['ds'].dt.quarter
        df['dayofyear'] = df['ds'].dt.dayofyear

        # Drop NaN rows
        df = df.dropna()

        return df

    def run_prophet(self) -> Dict:
        """Run Prophet with multiplicative seasonality and exogenous regressors."""
        print("  Running Prophet (with regressors)...")

        # Prepare data with regressors
        train_with_regressors = self.train_df.copy()

        # Add ALL exogenous features from segment data
        holiday_flag = self.segment_data['events']['holiday_flag']
        drop_flag = self.segment_data['events']['drop_flag']
        price = self.segment_data['observed']['price']
        hype = self.segment_data['ground_truth']['hype_lead14']
        marketing = self.segment_data['ground_truth']['marketing_lead7']

        train_with_regressors['holiday_flag'] = holiday_flag[:len(train_with_regressors)]
        train_with_regressors['drop_flag'] = drop_flag[:len(train_with_regressors)]
        train_with_regressors['price'] = price[:len(train_with_regressors)]
        train_with_regressors['hype'] = hype[:len(train_with_regressors)]
        train_with_regressors['marketing'] = marketing[:len(train_with_regressors)]

        model = Prophet(
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0,
            interval_width=0.95
        )

        model.add_country_holidays(country_name='US')

        # Add all regressors
        model.add_regressor('holiday_flag')
        model.add_regressor('drop_flag')
        model.add_regressor('price')
        model.add_regressor('hype')
        model.add_regressor('marketing')

        model.fit(train_with_regressors)

        # Create future dataframe with regressors
        future = model.make_future_dataframe(periods=self.test_horizon, freq=self.freq)

        # Add ALL regressor values for future periods
        future['holiday_flag'] = holiday_flag[:len(future)]
        future['drop_flag'] = drop_flag[:len(future)]
        future['price'] = price[:len(future)]
        future['hype'] = hype[:len(future)]
        future['marketing'] = marketing[:len(future)]

        forecast = model.predict(future)

        # Extract test predictions
        forecast_test = forecast.iloc[-self.test_horizon:]

        return {
            'yhat': forecast_test['yhat'].values,
            'yhat_lower': forecast_test['yhat_lower'].values,
            'yhat_upper': forecast_test['yhat_upper'].values,
        }

    def run_statsforecast(self) -> Dict:
        """Run StatsForecast AutoARIMA and AutoETS."""
        print("  Running StatsForecast (AutoARIMA, AutoETS, SeasonalNaive)...")

        # Prepare data for statsforecast (needs unique_id column)
        sf_df = self.train_df.copy()
        sf_df['unique_id'] = 'segment'
        sf_df = sf_df[['unique_id', 'ds', 'y']]

        # Initialize models
        models = [
            AutoARIMA(season_length=7),  # Weekly seasonality
            AutoETS(season_length=7),
            SeasonalNaive(season_length=7),
            Naive(),
        ]

        sf = StatsForecast(
            models=models,
            freq=self.freq,
            n_jobs=1
        )

        sf.fit(sf_df)
        forecast = sf.predict(h=self.test_horizon, level=[95])

        return {
            'AutoARIMA': {
                'yhat': forecast['AutoARIMA'].values,
                'yhat_lower': forecast['AutoARIMA-lo-95'].values,
                'yhat_upper': forecast['AutoARIMA-hi-95'].values,
            },
            'AutoETS': {
                'yhat': forecast['AutoETS'].values,
                'yhat_lower': forecast['AutoETS-lo-95'].values,
                'yhat_upper': forecast['AutoETS-hi-95'].values,
            },
            'SeasonalNaive': {
                'yhat': forecast['SeasonalNaive'].values,
            },
            'Naive': {
                'yhat': forecast['Naive'].values,
            }
        }

    def run_xgboost(self) -> Dict:
        """Run XGBoost with lag features using walk-forward validation (realistic: uses actual lags)."""
        print("  Running XGBoost (walk-forward with actuals)...")

        # Create features for training
        train_feat = self._create_lag_features(self.train_df)
        feature_cols = [c for c in train_feat.columns if c not in ['ds', 'y']]

        X_train = train_feat[feature_cols]
        y_train = train_feat['y']

        # Train model
        model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        # Walk-forward prediction with ACTUAL values for lags (realistic)
        predictions = []
        history_df = self.df.iloc[:-self.test_horizon].copy()  # Start with training data

        for i in range(self.test_horizon):
            # Create features using only historical data
            feat = self._create_lag_features(history_df)
            if len(feat) == 0:
                # Not enough history to create features
                predictions.append(history_df['y'].mean())
                continue

            # Get the last row (most recent features)
            X_current = feat[feature_cols].iloc[[-1]]

            # Predict next value
            pred = model.predict(X_current)[0]
            predictions.append(pred)

            # Add ACTUAL value to history (realistic: we know yesterday's actuals in production)
            next_date = self.test_df.iloc[i]['ds']
            actual_value = self.test_df.iloc[i]['y']
            next_row = pd.DataFrame({'ds': [next_date], 'y': [actual_value]})
            history_df = pd.concat([history_df, next_row], ignore_index=True)

        return {
            'yhat': np.array(predictions),
        }

    def run_lightgbm(self) -> Dict:
        """Run LightGBM with lag features using walk-forward validation (realistic: uses actual lags)."""
        print("  Running LightGBM (walk-forward with actuals)...")

        # Create features for training
        train_feat = self._create_lag_features(self.train_df)
        feature_cols = [c for c in train_feat.columns if c not in ['ds', 'y']]

        X_train = train_feat[feature_cols]
        y_train = train_feat['y']

        # Train model
        model = lgb.LGBMRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbosity=-1
        )

        model.fit(X_train, y_train)

        # Walk-forward prediction (no data leakage)
        predictions = []
        history_df = self.df.iloc[:-self.test_horizon].copy()  # Start with training data

        for i in range(self.test_horizon):
            # Create features using only historical data
            feat = self._create_lag_features(history_df)
            if len(feat) == 0:
                # Not enough history to create features
                predictions.append(history_df['y'].mean())
                continue

            # Get the last row (most recent features)
            X_current = feat[feature_cols].iloc[[-1]]

            # Predict next value
            pred = model.predict(X_current)[0]
            predictions.append(pred)

            # Add ACTUAL value to history (realistic: we know yesterday's actuals in production)
            next_date = self.test_df.iloc[i]['ds']
            actual_value = self.test_df.iloc[i]['y']
            next_row = pd.DataFrame({'ds': [next_date], 'y': [actual_value]})
            history_df = pd.concat([history_df, next_row], ignore_index=True)

        return {
            'yhat': np.array(predictions),
        }

    def compute_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, y_lower: np.ndarray = None, y_upper: np.ndarray = None) -> Dict:
        """Compute evaluation metrics."""
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        # MAPE with floor
        mape = np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 5.0))) * 100

        # Bias
        bias = np.mean(y_pred - y_true)

        # Coverage (if intervals provided)
        coverage = None
        if y_lower is not None and y_upper is not None:
            in_bounds = (y_lower <= y_true) & (y_true <= y_upper)
            coverage = in_bounds.mean()

        return {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape),
            'bias': float(bias),
            'coverage': float(coverage) if coverage is not None else None
        }

    def run_all(self) -> Dict:
        """Run all models and return results."""
        y_true = self.test_df['y'].values

        results = {}

        # Prophet
        try:
            prophet_result = self.run_prophet()
            results['Prophet'] = {
                'predictions': prophet_result,
                'metrics': self.compute_metrics(
                    y_true,
                    prophet_result['yhat'],
                    prophet_result['yhat_lower'],
                    prophet_result['yhat_upper']
                )
            }
        except Exception as e:
            print(f"    Prophet failed: {e}")
            results['Prophet'] = {'error': str(e)}

        # StatsForecast
        try:
            sf_results = self.run_statsforecast()

            for model_name, pred_data in sf_results.items():
                results[model_name] = {
                    'predictions': pred_data,
                    'metrics': self.compute_metrics(
                        y_true,
                        pred_data['yhat'],
                        pred_data.get('yhat_lower'),
                        pred_data.get('yhat_upper')
                    )
                }
        except Exception as e:
            print(f"    StatsForecast failed: {e}")

        # XGBoost
        try:
            xgb_result = self.run_xgboost()
            results['XGBoost'] = {
                'predictions': xgb_result,
                'metrics': self.compute_metrics(y_true, xgb_result['yhat'])
            }
        except Exception as e:
            print(f"    XGBoost failed: {e}")
            results['XGBoost'] = {'error': str(e)}

        # LightGBM
        try:
            lgb_result = self.run_lightgbm()
            results['LightGBM'] = {
                'predictions': lgb_result,
                'metrics': self.compute_metrics(y_true, lgb_result['yhat'])
            }
        except Exception as e:
            print(f"    LightGBM failed: {e}")
            results['LightGBM'] = {'error': str(e)}

        return results


def benchmark_all_segments(data_dir: Path = Path("./data")) -> pd.DataFrame:
    """
    Run benchmark on all segments and return summary DataFrame.
    """
    json_files = sorted(data_dir.glob("AirJordan_*.json"))

    all_results = []

    for json_file in json_files:
        print(f"\nBenchmarking {json_file.stem}...")

        with open(json_file, 'r') as f:
            segment_data = json.load(f)

        benchmark = ForecastBenchmark(segment_data, test_horizon=56)
        results = benchmark.run_all()

        # Extract metrics for each model
        for model_name, model_result in results.items():
            if 'metrics' in model_result:
                metrics = model_result['metrics']
                all_results.append({
                    'segment': json_file.stem,
                    'model': model_name,
                    'mae': metrics['mae'],
                    'rmse': metrics['rmse'],
                    'mape': metrics['mape'],
                    'bias': metrics['bias'],
                    'coverage': metrics.get('coverage'),
                })

    return pd.DataFrame(all_results)


def main():
    """Run full benchmark."""
    print("="*60)
    print("MODEL BENCHMARK: Air Jordan Demand Forecasting")
    print("="*60)

    results_df = benchmark_all_segments()

    # Save results
    results_df.to_csv("benchmark_results.csv", index=False)
    print(f"\n✓ Saved benchmark_results.csv")

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY: Average Metrics Across All Segments")
    print("="*60)

    summary = results_df.groupby('model').agg({
        'mae': 'mean',
        'rmse': 'mean',
        'mape': 'mean',
        'bias': 'mean',
        'coverage': 'mean'
    }).round(2)

    summary = summary.sort_values('mae')
    print(summary.to_string())

    print("\n" + "="*60)
    print("WINNER (Lowest MAE):")
    print("="*60)
    best_model = summary.index[0]
    print(f"{best_model}: MAE={summary.loc[best_model, 'mae']:.2f}, MAPE={summary.loc[best_model, 'mape']:.1f}%")


if __name__ == "__main__":
    main()
