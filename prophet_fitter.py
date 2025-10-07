"""
Prophet Model Fitting and Backtesting

Fits Prophet models with multiplicative seasonality and runs rolling-origin backtests.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from prophet import Prophet
import warnings

warnings.filterwarnings('ignore')


class ProphetFitter:
    """
    Fit Prophet models and compute backtest metrics.
    """

    def __init__(
        self,
        seasonality_mode: str = "multiplicative",
        changepoint_prior_scale: float = 0.05,
        seasonality_prior_scale: float = 10.0,
    ):
        """
        Initialize fitter.

        Args:
            seasonality_mode: 'multiplicative' or 'additive'
            changepoint_prior_scale: Flexibility of trend
            seasonality_prior_scale: Strength of seasonality
        """
        self.seasonality_mode = seasonality_mode
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale

    def fit_segment(
        self,
        segment_data: Dict,
        add_holidays: bool = True,
    ) -> Dict:
        """
        Fit Prophet to a single segment.

        Args:
            segment_data: Segment data dict
            add_holidays: Include US holidays

        Returns:
            Updated segment_data with prophet predictions
        """
        # Prepare data for Prophet
        df = pd.DataFrame({
            'ds': pd.to_datetime(segment_data['calendar']['ds']),
            'y': segment_data['observed']['units']
        })

        # Initialize model
        model = Prophet(
            seasonality_mode=self.seasonality_mode,
            changepoint_prior_scale=self.changepoint_prior_scale,
            seasonality_prior_scale=self.seasonality_prior_scale,
            interval_width=0.95,
        )

        # Add US holidays
        if add_holidays:
            model.add_country_holidays(country_name='US')

        # Fit
        model.fit(df)

        # Predict on full history
        forecast = model.predict(df)

        # Extract components
        segment_data['prophet'] = {
            'yhat': forecast['yhat'].tolist(),
            'yhat_lower': forecast['yhat_lower'].tolist(),
            'yhat_upper': forecast['yhat_upper'].tolist(),
            'trend': forecast['trend'].tolist(),
            'weekly': forecast.get('weekly', pd.Series([0] * len(df))).tolist(),
            'yearly': forecast.get('yearly', pd.Series([0] * len(df))).tolist(),
            'holidays': forecast.get('holidays', pd.Series([0] * len(df))).tolist(),
        }

        return segment_data

    def backtest_segment(
        self,
        segment_data: Dict,
        horizon_days: int = 56,
        n_folds: int = 4,
        add_holidays: bool = True,
    ) -> Dict:
        """
        Run rolling-origin backtest and compute metrics.

        Args:
            segment_data: Segment data dict
            horizon_days: Forecast horizon in days
            n_folds: Number of backtest folds
            add_holidays: Include US holidays

        Returns:
            Updated segment_data with metrics
        """
        df = pd.DataFrame({
            'ds': pd.to_datetime(segment_data['calendar']['ds']),
            'y': segment_data['observed']['units']
        })

        freq = segment_data['meta']['freq']
        horizon_periods = horizon_days if freq == 'D' else (horizon_days // 7)

        # Compute fold cutoffs
        total_periods = len(df)
        test_size = horizon_periods
        train_min = total_periods // 2  # Use at least half the data for training

        cutoffs = []
        for fold in range(n_folds):
            cutoff_idx = total_periods - test_size * (n_folds - fold)
            if cutoff_idx >= train_min:
                cutoffs.append(df['ds'].iloc[cutoff_idx])

        if len(cutoffs) == 0:
            print(f"Warning: Not enough data for {n_folds} folds, using 1 fold")
            cutoffs = [df['ds'].iloc[total_periods - test_size]]

        # Run folds
        all_errors = []
        all_actuals = []
        all_predictions = []
        all_in_bounds = []

        for cutoff in cutoffs:
            train_df = df[df['ds'] <= cutoff].copy()
            test_df = df[df['ds'] > cutoff].head(horizon_periods).copy()

            if len(test_df) == 0:
                continue

            # Fit model
            model = Prophet(
                seasonality_mode=self.seasonality_mode,
                changepoint_prior_scale=self.changepoint_prior_scale,
                seasonality_prior_scale=self.seasonality_prior_scale,
                interval_width=0.95,
            )

            if add_holidays:
                model.add_country_holidays(country_name='US')

            model.fit(train_df)

            # Predict
            future = model.make_future_dataframe(periods=len(test_df), freq=freq)
            forecast = model.predict(future)
            forecast = forecast[forecast['ds'] > cutoff].head(horizon_periods)

            # Align
            test_df = test_df.merge(
                forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
                on='ds',
                how='inner'
            )

            # Collect metrics
            actuals = test_df['y'].values
            preds = test_df['yhat'].values
            lower = test_df['yhat_lower'].values
            upper = test_df['yhat_upper'].values

            all_actuals.extend(actuals)
            all_predictions.extend(preds)
            all_errors.extend(actuals - preds)
            all_in_bounds.extend([(lower[i] <= actuals[i] <= upper[i]) for i in range(len(actuals))])

        # Compute aggregated metrics
        all_actuals = np.array(all_actuals)
        all_predictions = np.array(all_predictions)
        all_errors = np.array(all_errors)
        all_in_bounds = np.array(all_in_bounds)

        mae = np.mean(np.abs(all_errors))

        # MAPE with floor to avoid division by near-zero
        # Use max(actual, 5) as denominator to avoid inflation
        mape = np.mean(np.abs(all_errors / np.maximum(all_actuals, 5.0))) * 100  # percentage

        bias = np.mean(all_errors)
        coverage = np.mean(all_in_bounds)

        segment_data['metrics'] = {
            'backtest': {
                'horizon_days': horizon_days,
                'folds': len(cutoffs),
                'window': 'rolling_origin',
            },
            'mae': round(float(mae), 2),
            'mape': round(float(mape), 2),
            'bias': round(float(bias), 2),
            'coverage': round(float(coverage), 3),
        }

        return segment_data

    def fit_and_backtest_all(
        self,
        segments_data: List[Dict],
        horizon_days: int = 56,
        n_folds: int = 4,
        add_holidays: bool = True,
    ) -> List[Dict]:
        """
        Fit Prophet and run backtests for all segments.

        Args:
            segments_data: List of segment data dicts
            horizon_days: Forecast horizon
            n_folds: Number of backtest folds
            add_holidays: Include holidays

        Returns:
            Updated segments_data with prophet forecasts and metrics
        """
        for i, segment_data in enumerate(segments_data):
            segment_name = segment_data['meta']['segment']
            print(f"[{i+1}/{len(segments_data)}] Fitting {segment_name}...")

            # Fit
            segment_data = self.fit_segment(segment_data, add_holidays=add_holidays)

            # Backtest
            segment_data = self.backtest_segment(
                segment_data,
                horizon_days=horizon_days,
                n_folds=n_folds,
                add_holidays=add_holidays
            )

            # Print metrics
            metrics = segment_data['metrics']
            print(f"  MAE: {metrics['mae']:.1f}, MAPE: {metrics['mape']:.1f}%, "
                  f"Bias: {metrics['bias']:.1f}, Coverage: {metrics['coverage']:.2f}")

        return segments_data
