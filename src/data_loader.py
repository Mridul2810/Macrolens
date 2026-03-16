import yfinance as yf
import pandas as pd
from fredapi import Fred
from src.config import SECTOR_ETFS, BENCHMARK, START_DATE, END_DATE, FRED_SERIES


def download_market_data():
    tickers = SECTOR_ETFS + [BENCHMARK]

    data = yf.download(
        tickers,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False
    )["Close"]

    return data


def download_fred_data(api_key):
    fred = Fred(api_key=api_key)
    macro = pd.DataFrame()

    for name, series_id in FRED_SERIES.items():
        macro[name] = fred.get_series(series_id)

    return macro