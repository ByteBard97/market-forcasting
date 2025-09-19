# Market Forecasting Tool

A retail sales forecasting application designed to help business analysts predict next year's sales by franchise/silo, compare multiple forecasting models, and run what-if scenarios.

## Project Overview

This tool aims to provide non-technical business users with an intuitive interface to:
- Upload retail sales data (CSV/Excel)
- Run multiple forecasting models in parallel
- Compare model performance and accuracy
- Adjust scenario parameters (promotions, pricing, foot traffic)
- Export forecasts and visualizations

## Implementation Approaches

### Option 1: Vue.js Web Application (Simple Time Series)
**Best for:** Basic forecasting needs without heavy ML requirements

**Tech Stack:**
- Frontend: Vue 3 + Vite
- Charts: ECharts or Plotly.js
- File handling: SheetJS (Excel) + Papa Parse (CSV)
- Forecasting: JavaScript-based time series models (exponential smoothing, simple ARIMA)
- Deployment: Static web app or wrapped as desktop app with Tauri

**Features:**
- Drag-and-drop file upload
- Interactive scenario sliders
- Model comparison overlays
- CSV/PDF export

### Option 2: PyQt6 Desktop Application (Advanced ML)
**Best for:** Sophisticated forecasting with machine learning models

**Tech Stack:**
- UI: PyQt6
- Backend: Python with statsmodels, Prophet, XGBoost, LightGBM
- Data processing: pandas, numpy
- Packaging: PyInstaller/Briefcase for Mac executable

**Features:**
- Full ML model suite (ARIMA/SARIMA, Prophet, gradient boosting)
- Advanced backtesting and cross-validation
- Feature engineering capabilities
- Comprehensive error metrics (MAPE, RMSE, MASE)
- Offline operation with all processing local

## Data Requirements

Expected input format (CSV/Excel):
- `date`: Time period (monthly/weekly)
- `franchise_id`: Store/franchise identifier
- `silo`: Business segment
- `net_sales`: Sales figures
- `promo_flag`: Promotion indicator (optional)
- `price_index`: Pricing data (optional)
- `foot_traffic_idx`: Traffic metrics (optional)
- `holiday_flag`: Holiday periods (optional)

Minimum: 24 periods of historical data for seasonal analysis

## Models Supported

### Basic Models
- Naive seasonal baseline
- Exponential smoothing (Holt-Winters)
- Simple moving averages

### Advanced Models (PyQt6 version only)
- ARIMA/SARIMA with auto-tuning
- Facebook Prophet
- XGBoost/LightGBM with feature engineering
- Ensemble methods

## Evaluation Metrics
- MAPE (Mean Absolute Percentage Error)
- RMSE (Root Mean Square Error)
- MAE (Mean Absolute Error)
- sMAPE (Symmetric MAPE)
- Prediction interval coverage

## Next Steps

1. Complete requirements gathering interview with stakeholder
2. Determine complexity level needed (basic vs. advanced ML)
3. Choose implementation path based on requirements
4. Build MVP with core functionality
5. Iterate based on user feedback

## Development Status

🚧 **In Planning Phase** - Currently gathering requirements and determining optimal technical approach
