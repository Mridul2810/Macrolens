import pandas as pd
from src.config import SECTOR_ETFS, BENCHMARK, TRANSACTION_COST
from src.portfolio import get_weights_for_regime


def run_backtest(df):
    df = df.copy()

    portfolio_returns = []
    benchmark_returns = []
    regimes = []
    prev_weights = None

    for date, row in df.iterrows():
        regime = row["regime"]
        weights = get_weights_for_regime(regime)

        port_ret = 0
        for etf in SECTOR_ETFS:
            port_ret += weights.get(etf, 0) * row[etf]

        turnover = 0
        if prev_weights is not None:
            all_keys = set(weights.keys()).union(prev_weights.keys())
            turnover = sum(abs(weights.get(k, 0) - prev_weights.get(k, 0)) for k in all_keys)

        net_ret = port_ret - TRANSACTION_COST * turnover

        portfolio_returns.append(net_ret)
        benchmark_returns.append(row[BENCHMARK])
        regimes.append(regime)

        prev_weights = weights

    results = pd.DataFrame({
        "portfolio_return": portfolio_returns,
        "benchmark_return": benchmark_returns,
        "regime": regimes
    }, index=df.index)

    results["portfolio_growth"] = (1 + results["portfolio_return"]).cumprod()
    results["benchmark_growth"] = (1 + results["benchmark_return"]).cumprod()

    return results