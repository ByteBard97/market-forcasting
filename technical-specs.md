# Technical Specifications - Market Forecasting Tool

## Product Manager Interview Script Sections
Key questions to gather from stakeholder:
1. Context & Goals - Problem to solve, primary/secondary goals
2. Users & Access - Who uses it, access model, permissions
3. Data Inventory - Time grain, entities, measures, formats, quality
4. Forecasting Scope - Frequency, horizon, aggregation, scenario knobs
5. Models to Compare - Classical vs ML preferences
6. Evaluation & Good Enough - Metrics, acceptance thresholds
7. Outputs & UX - Views, KPIs, exports
8. Workflow - Ingestion, mapping, save/load
9. Privacy & Compliance
10. Deployment & Ops - Platform, hosting, auth
11. Timeline & Success Criteria

## API Design

### POST /fit_and_forecast
```json
{
  "series": [
    {
      "key": {"franchise_id":"F001","silo":"Core"},
      "date": ["2022-01-01","..."],
      "y": [15234, ...],
      "exog": {
        "promo_flag": [0,1,...],
        "price_index": [1.02,...],
        "foot_traffic_idx": [0.98,...]
      }
    }
  ],
  "horizon": 12,
  "models": [
    {"name":"seasonal_hw", "params":{"seasonal":"mul","period":12}},
    {"name":"auto_arima", "params":{"seasonal":true,"m":12}},
    {"name":"xgboost", "params":{"lags": [1,2,12], "rolling_mean":[4,12]}},
    {"name":"prophet", "params":{"yearly_seasonality":true}}
  ],
  "backtest": {"folds": 4, "stride": 3, "test_size": 6},
  "return_pi": [0.8, 0.95]
}
```

## Model Performance Guidelines

### Processing Times (per series)
- Holt-Winters/ETS: ~0.05–0.3s
- SARIMA (fixed params): ~0.1–0.7s
- Auto-ARIMA (seasonal search): ~0.5–6s
- Prophet: ~0.2–1.0s
- XGBoost: ~0.1–0.5s

### Data Scale Recommendations
- **Small** (100 series × 60 pts): All models, 3 folds - instant to minutes
- **Medium** (300-600 series × 60-120 pts): Cap ARIMA search, 2-3 folds - minutes
- **Large** (1000-3000 series): Global XGB + per-series ETS/ARIMA for top-K - tens of minutes
- **Very Large** (10k+ series): Cloud/cluster or aggressive sampling

## Model Selection Matrix

| Data Situation | Few Points (<30-40) | Medium Length (50-500) | Long Sequences (500+) |
|----------------|-------------------|----------------------|---------------------|
| **Single/Few Series** | ETS/Holt-Winters, Auto-ARIMA | Same + Prophet | ARIMA/SARIMA or state-space |
| **Dozens-Hundreds Series** | Aggregate or per-series ARIMA/ETS | N-BEATS/N-HiTS (global), XGBoost/MLP with lags | TFT, DeepAR |
| **Thousands+ Series** | Hierarchical ETS | Global XGBoost/LightGBM + top-K individuals | Deep learning required |

## Python Libraries

### Core Dependencies
- **FastAPI**: REST API framework
- **statsmodels**: ARIMA, SARIMA, ETS
- **pmdarima**: Auto-ARIMA with seasonal detection
- **prophet**: Facebook's forecasting library
- **xgboost/lightgbm**: Gradient boosting
- **darts**: Unified forecasting API (optional for N-BEATS, TFT)

### Frontend (Vue)
- **SheetJS**: Excel file parsing
- **Papa Parse**: CSV parsing
- **ECharts/Plotly**: Interactive charts
- **Tauri**: Desktop app wrapper (optional)

## Data Requirements

### Business Data Characteristics
- Usually monthly/weekly aggregations
- May have irregular gaps (store closures, holidays)
- Needs regularization for time series models
- Common issues: promotions, stockouts, new products

### Required Preprocessing
1. Regularize to consistent intervals (resample/interpolate)
2. Handle missing values (forward fill, interpolation)
3. Detect and handle outliers
4. Normalize seasonality patterns

## Evaluation Metrics
- **MAPE**: Mean Absolute Percentage Error (business favorite)
- **RMSE**: Root Mean Square Error
- **MAE**: Mean Absolute Error
- **sMAPE**: Symmetric MAPE
- **WAPE**: Weighted Absolute Percentage Error
- **PI Coverage**: Prediction interval accuracy (should be ~95% for 95% PI)

## Backtesting Strategy
**Rolling-Origin Cross-Validation**:
- Train up to time t
- Test next k periods (e.g., 6 months)
- Roll forward by stride
- Aggregate metrics across folds

## Optimization Tips
1. **Cap ARIMA search**: max_p,max_q ≤ 3, stepwise=True
2. **Prefer ETS baseline**: Add ARIMA only where ETS underperforms
3. **Reduce folds**: 2-3 folds with 6-12 month windows sufficient
4. **Global models**: Train one XGBoost across all series with entity features
5. **Selective per-series**: Run individual models only on top revenue drivers

## External Data Sources
- **Holidays**: workalendar, pandas-market-calendars
- **Weather**: NOAA, meteostat APIs
- **Macro**: FRED (CPI, Retail Sales Index, Consumer Confidence)
- **Events**: Local calendars, sports schedules

## PyQt6 Implementation Notes
- **Charts**: Plotly in QWebEngineView, pyqtgraph for fast residuals
- **Compute**: QThreadPool for parallel model fitting
- **Packaging**: PyInstaller/Briefcase for Mac .app
- **Performance**: Cache fitted models, cap auto-ARIMA search

## Alternative Architectures Considered
1. **Google Sheets + Apps Script**: Zero install, 100k row limit
2. **PyQt6 + PyInstaller**: All Python local, larger binary
3. **Vue + Tauri + FastAPI**: Best balance, clean separation
4. **Pure web app**: Requires hosting, best for multi-user

## Success Criteria
- MAPE ≤ 12% at monthly company total
- 95% prediction intervals cover ~93-97% of actuals
- Recompute scenarios < 2s for 500 stores × 36 months
- Export to Excel/PDF in one click