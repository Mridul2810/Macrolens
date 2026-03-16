import pandas as pd


def load_raw_data():
    market = pd.read_csv("data/raw/market_data.csv", index_col=0, parse_dates=True)
    macro = pd.read_csv("data/raw/macro_data.csv", index_col=0, parse_dates=True)
    return market, macro


def prepare_monthly_data(market, macro):
    monthly_prices = market.resample("ME").last()
    monthly_returns = monthly_prices.pct_change()

    macro_monthly = macro.resample("ME").last().ffill()

    df = monthly_returns.join(macro_monthly, how="inner")
    df = df.dropna()

    return df, monthly_prices