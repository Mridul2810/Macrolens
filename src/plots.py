import os
import matplotlib.pyplot as plt


def plot_growth(results):
    os.makedirs("results", exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(results.index, results["portfolio_growth"], label="Portfolio")
    plt.plot(results.index, results["benchmark_growth"], label="Benchmark (SPY)")
    plt.title("Portfolio vs Benchmark Growth")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/growth_chart.png")
    plt.close()


def plot_regimes(results):
    os.makedirs("results", exist_ok=True)

    regime_counts = results["regime"].value_counts()

    plt.figure(figsize=(8, 5))
    regime_counts.plot(kind="bar")
    plt.title("Number of Months in Each Regime")
    plt.xlabel("Regime")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("results/regime_counts.png")
    plt.close()

def plot_drawdown(results):
    os.makedirs("results", exist_ok=True)

    portfolio_running_max = results["portfolio_growth"].cummax()
    benchmark_running_max = results["benchmark_growth"].cummax()

    portfolio_drawdown = (results["portfolio_growth"] - portfolio_running_max) / portfolio_running_max
    benchmark_drawdown = (results["benchmark_growth"] - benchmark_running_max) / benchmark_running_max

    plt.figure(figsize=(10, 6))
    plt.plot(results.index, portfolio_drawdown, label="Portfolio Drawdown")
    plt.plot(results.index, benchmark_drawdown, label="Benchmark Drawdown")
    plt.title("Drawdown: Portfolio vs Benchmark")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/drawdown_chart.png")
    plt.close()