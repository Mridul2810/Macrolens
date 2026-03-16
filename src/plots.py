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