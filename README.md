# 🇮🇳 India Population Forecast Dashboard (1950 - 2050)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/ML-Ridge_Polynomial_Regression-purple.svg)](#)

A high-performance codebase and ultra-premium interactive dashboard for forecasting India's macro population trends spanning an exact century of data. 

---

## ✨ Features

- **Ultra-Premium Dashboard**: A beautifully designed frontend built with Streamlit, entirely overhauled with custom CSS, animated space gradients, and pure glassmorphism.
- **Machine Learning Integration**: Powered by a robust Ridge Polynomial Regression (Degree 5) model that mathematically balances complex demographic shifts.
- **Flawless Gender Mathematics**: The model structure guarantees that `Male + Female = Total` at any projected point by predicting Total & Male trajectories securely, and deriving Female trajectories statistically.
- **Interactive Visualizations**: Leveraging **Plotly Express & Graph Objects**, the app includes interactive spline-curve line charts, dynamically shaded area distributions, and metric KPI deltas that calculate Year-over-Year (YoY) growth on the fly.
- **Production Ready**: Optimized `@st.cache_data` memory management guarantees instant responsiveness across 100 years of data.

---

## 🛠️ Data Architecture

The repository contains historical data (from official metrics, 1950-2025) and model-generated predictions (2026-2050). 

| File | Purpose |
| :--- | :--- |
| `india_population_complete_1950_2050.csv` | The master dataset spanning the complete 100-year history and valid forecast. Used seamlessly by the Dashboard app. |
| `population_prediction.ipynb` | The core Jupyter Notebook carrying the Exploratory Data Analysis, Hyperparameter Tuning (GridSearchCV), and Cross-Validation model training processes. |
| `app.py` | The main Streamlit web application orchestrating the UI and visualizations. |
| `requirements.txt` | Dependency locker for perfect reproducible environments and Streamlit Cloud integrations. |

---

## 🚀 Quickstart & Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/india-population-forecast.git
cd india-population-forecast
```

**2. Install Dependencies**
It is recommended you use a virtual environment.
```bash
pip install -r requirements.txt
```

**3. Run the App**
To launch the Ultra-Premium dashboard locally:
```bash
streamlit run app.py
```
*Navigate your browser to `http://localhost:8501` to view your dashboard!*

---

## 🔬 Model Performance Statistics

Our cross-validated ML estimators scored excellent metrics against test sets preventing both under-fitting and over-fitting:

*   **Total Population Test R²**: `0.9390` (MAPE `1.37%`)
*   **Female Population Test R²**: `0.9558` (MAPE `1.19%`)
*   **Male Population Test R²**: `0.7411` (MAPE `2.45%`)

---

## ☁️ Deployment

Ready for out-of-the-box deployment to Streamlit Community Cloud:
1. Push your code to GitHub.
2. Sign in to Streamlit Share.
3. Hook your repository and enter `app.py` as your main file path!

*(No extra configuration is required, Streamlit will automatically read `requirements.txt`)*

---

***Developed by Hiten*** 🚀
