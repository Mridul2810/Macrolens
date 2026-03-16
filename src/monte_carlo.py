import numpy as np
import pandas as pd


def simulate_paths(returns, n_simulations=1000, n_months=12, initial_value=1.0):
    returns = returns.dropna()

    mean_return = returns.mean()
    std_return = returns.std()

    simulated_paths = []

    for _ in range(n_simulations):
        random_returns = np.random.normal(mean_return, std_return, n_months)
        path = [initial_value]

        for r in random_returns:
            path.append(path[-1] * (1 + r))

        simulated_paths.append(path)

    paths_df = pd.DataFrame(simulated_paths).T
    return paths_df


def compute_drawdown(path_values):
    running_max = np.maximum.accumulate(path_values)
    drawdowns = (path_values - running_max) / running_max
    return drawdowns.min()


def monte_carlo_summary(portfolio_returns, benchmark_returns, n_simulations=1000, n_months=12):
    portfolio_paths = simulate_paths(portfolio_returns, n_simulations=n_simulations, n_months=n_months)
    benchmark_paths = simulate_paths(benchmark_returns, n_simulations=n_simulations, n_months=n_months)

    portfolio_final = portfolio_paths.iloc[-1]
    benchmark_final = benchmark_paths.iloc[-1]

    prob_loss = (portfolio_final < 1.0).mean()
    prob_beat_benchmark = (portfolio_final > benchmark_final).mean()

    portfolio_drawdowns = portfolio_paths.apply(compute_drawdown, axis=0)
    prob_drawdown_worse_than_15 = (portfolio_drawdowns < -0.15).mean()

    summary = pd.Series({
        "Probability of Loss (12M)": prob_loss,
        "Probability of Beating Benchmark (12M)": prob_beat_benchmark,
        "Probability of Drawdown Worse Than -15%": prob_drawdown_worse_than_15,
        "Portfolio Final Value 5th Percentile": portfolio_final.quantile(0.05),
        "Portfolio Final Value Median": portfolio_final.quantile(0.50),
        "Portfolio Final Value 95th Percentile": portfolio_final.quantile(0.95),
    })

    return summary, portfolio_paths, benchmark_paths