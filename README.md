# MacroLens

MacroLens is a regime-based portfolio strategy project that uses macroeconomic indicators to classify market environments and allocate sector ETFs accordingly.

## Project Overview
This project combines macroeconomic data and market data to test whether different economic environments can guide sector allocation decisions. The strategy assigns portfolio weights based on regimes such as Growth, Inflationary, Defensive, and Mixed, then compares performance against SPY.

## Features
- Downloads sector ETF price data using Yahoo Finance
- Downloads macroeconomic data from FRED
- Cleans and aligns market and macro data at monthly frequency
- Defines market regimes using inflation, yield spread, and interest rates
- Assigns portfolio weights based on regime
- Runs a backtest with transaction costs
- Calculates performance metrics such as annual return, volatility, Sharpe ratio, max drawdown, and hit rate
- Displays results in a Streamlit dashboard

## Assets Used
- XLF
- XLK
- XLE
- XLV
- XLI
- XLP
- XLU
- XLY
- SPY as benchmark

## Macro Variables Used
- CPI
- Unemployment Rate
- Federal Funds Rate
- 10-Year Treasury Rate
- 2-Year Treasury Rate

## Regimes
- **Growth**: lower-rate / non-inverted conditions
- **Inflationary**: high inflation and high rates
- **Defensive**: inverted curve and high inflation
- **Mixed**: all other cases

## Tech Stack
- Python
- pandas
- numpy
- matplotlib
- yfinance
- fredapi
- statsmodels
- scipy
- streamlit

## How to Run

### 1. Activate the virtual environment
```bash
source .venv/bin/activate