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

st.subheader("Performance Summary")
st.dataframe(summary)

st.subheader("Growth of $1")
st.line_chart(results[["portfolio_growth", "benchmark_growth"]])

st.subheader("Monthly Returns")
st.line_chart(results[["portfolio_return", "benchmark_return"]])

st.subheader("Regime Distribution")
regime_counts = results["regime"].value_counts()
st.bar_chart(regime_counts)

st.subheader("Recent Backtest Data")
st.dataframe(results.tail(20))