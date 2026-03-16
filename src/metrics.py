import numpy as np
import pandas as pd


def annualized_return(returns):
    returns = returns.dropna()
    n = len(returns)
    if n == 0:
        return np.nan
    total_growth = (1 + returns).prod()
    return total_growth ** (12 / n) - 1


def annualized_volatility(returns):
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan
    return returns.std() * np.sqrt(12)


def sharpe_ratio(returns, risk_free_rate=0.0):
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan
    excess = returns - risk_free_rate / 12
    vol = excess.std()
    if vol == 0:
        return np.nan
    return (excess.mean() / vol) * np.sqrt(12)


def max_drawdown(growth_series):
    growth_series = growth_series.dropna()
    if len(growth_series) == 0:
        return np.nan
    running_max = growth_series.cummax()
    drawdown = (growth_series - running_max) / running_max
    return drawdown.min()


def hit_rate(returns):
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan
    return (returns > 0).mean()


def summarize_performance(results):
    summary = {
        "Portfolio Annual Return": annualized_return(results["portfolio_return"]),
        "Portfolio Annual Volatility": annualized_volatility(results["portfolio_return"]),
        "Portfolio Sharpe": sharpe_ratio(results["portfolio_return"]),
        "Portfolio Max Drawdown": max_drawdown(results["portfolio_growth"]),
        "Portfolio Hit Rate": hit_rate(results["portfolio_return"]),
        "Benchmark Annual Return": annualized_return(results["benchmark_return"]),
        "Benchmark Annual Volatility": annualized_volatility(results["benchmark_return"]),
        "Benchmark Sharpe": sharpe_ratio(results["benchmark_return"]),
        "Benchmark Max Drawdown": max_drawdown(results["benchmark_growth"]),
        "Benchmark Hit Rate": hit_rate(results["benchmark_return"]),
    }

    return pd.Series(summary)