import pandas as pd
import streamlit as st

st.set_page_config(page_title="MacroLens Dashboard", layout="wide")

st.title("MacroLens: Regime-Based Portfolio Strategy")
st.write("This dashboard shows the backtest results of a macro regime-based sector allocation strategy.")

results = pd.read_csv("results/backtest_results.csv", index_col=0, parse_dates=True)

summary = pd.read_csv("results/performance_summary.csv", index_col=0, header=None)
summary.columns = ["Value"]
summary = summary.iloc[1:].copy()
summary.index = summary.index.astype(str)
summary.index.name = "Metric"
weights_history = pd.read_csv("results/weights_history.csv", index_col=0, parse_dates=True)

st.subheader("Performance Summary")
st.dataframe(summary)
st.subheader("Current Regime")
current_regime = results["regime"].iloc[-1]
st.write(f"**Latest detected regime:** {current_regime}")

st.subheader("Current Portfolio Weights")
current_weights = weights_history.iloc[-1].sort_values(ascending=False)
st.dataframe(current_weights[current_weights > 0])

st.subheader("Growth of $1")
st.line_chart(results[["portfolio_growth", "benchmark_growth"]])
st.subheader("Drawdown")
drawdown_df = pd.DataFrame(index=results.index)
drawdown_df["portfolio_drawdown"] = (
    results["portfolio_growth"] - results["portfolio_growth"].cummax()
) / results["portfolio_growth"].cummax()

drawdown_df["benchmark_drawdown"] = (
    results["benchmark_growth"] - results["benchmark_growth"].cummax()
) / results["benchmark_growth"].cummax()

st.line_chart(drawdown_df)

st.subheader("Rolling 12-Month Sharpe Ratio")

rolling_window = 12

rolling_sharpe = pd.DataFrame(index=results.index)

rolling_sharpe["portfolio_rolling_sharpe"] = (
    results["portfolio_return"].rolling(rolling_window).mean()
    / results["portfolio_return"].rolling(rolling_window).std()
) * (12 ** 0.5)

rolling_sharpe["benchmark_rolling_sharpe"] = (
    results["benchmark_return"].rolling(rolling_window).mean()
    / results["benchmark_return"].rolling(rolling_window).std()
) * (12 ** 0.5)

st.subheader("Rolling 12-Month Volatility")

rolling_vol = pd.DataFrame(index=results.index)

rolling_vol["portfolio_rolling_volatility"] = (
    results["portfolio_return"].rolling(12).std()
) * (12 ** 0.5)

rolling_vol["benchmark_rolling_volatility"] = (
    results["benchmark_return"].rolling(12).std()
) * (12 ** 0.5)

st.line_chart(rolling_vol)

st.line_chart(rolling_sharpe)

st.subheader("Monthly Returns")
st.line_chart(results[["portfolio_return", "benchmark_return"]])

st.subheader("Regime Distribution")
regime_counts = results["regime"].value_counts()
st.bar_chart(regime_counts)

st.subheader("Recent Backtest Data")
st.dataframe(results.tail(20))