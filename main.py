import os
from src.plots import plot_growth, plot_regimes, plot_drawdown
from src.data_loader import download_market_data, download_fred_data
from src.preprocess import load_raw_data, prepare_monthly_data
from src.regimes import add_regime_features, assign_regimes
from src.backtest import run_backtest
from src.metrics import summarize_performance


def download_and_save_raw_data():
    os.makedirs("data/raw", exist_ok=True)

    print("Downloading market data...")
    market = download_market_data()
    market.to_csv("data/raw/market_data.csv")

    api_key = os.getenv("FRED_API_KEY")
    if api_key is None:
        raise ValueError("FRED_API_KEY was not found. Please set it in Terminal first.")

    print("Downloading macro data from FRED...")
    macro = download_fred_data(api_key)
    macro.to_csv("data/raw/macro_data.csv")

    print("Raw data saved in data/raw/")


def run_pipeline():
    print("Loading raw data...")
    market, macro = load_raw_data()

    print("Preparing monthly data...")
    df, monthly_prices = prepare_monthly_data(market, macro)

    print("Adding regime features...")
    df = add_regime_features(df)

    print("Assigning regimes...")
    df = assign_regimes(df)

    df = df.dropna()

    print("Running backtest...")
    results, weights_df = run_backtest(df)

    print("Calculating performance summary...")
    summary = summarize_performance(results)
    print("Creating charts...")
    plot_growth(results)
    plot_regimes(results)
    plot_drawdown(results) 

    os.makedirs("results", exist_ok=True)
    results.to_csv("results/backtest_results.csv")
    summary.to_csv("results/performance_summary.csv")
    weights_df.to_csv("results/weights_history.csv")

    print("\nPerformance Summary:")
    print(summary)

    print("\nSaved:")
    print("- results/backtest_results.csv")
    print("- results/performance_summary.csv")
    print("- results/weights_history.csv")


def main():
    download_and_save_raw_data()
    run_pipeline()


if __name__ == "__main__":
    main()