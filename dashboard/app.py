import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="MacroLens Dashboard", layout="wide")

SECTOR_ETFS = ["XLF", "XLK", "XLE", "XLV", "XLI", "XLP", "XLU", "XLY"]
BENCHMARK = "SPY"
LIVE_TICKERS = SECTOR_ETFS + [BENCHMARK]


@st.cache_data(ttl=300)
def load_live_snapshot():
    data = yf.download(
        LIVE_TICKERS,
        period="5d",
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="ticker"
    )

    rows = []

    for ticker in LIVE_TICKERS:
        ticker_df = data[ticker].dropna()
        if len(ticker_df) == 0:
            continue

        latest_close = float(ticker_df["Close"].iloc[-1])

        if len(ticker_df) >= 2:
            prev_close = float(ticker_df["Close"].iloc[-2])
            daily_return = (latest_close / prev_close) - 1
        else:
            prev_close = latest_close
            daily_return = 0.0

        rows.append({
            "Ticker": ticker,
            "Latest Price": latest_close,
            "Previous Close": prev_close,
            "Daily Return": daily_return
        })

    return pd.DataFrame(rows)


# Manual refresh button
if st.button("Refresh live data now"):
    st.cache_data.clear()
    st.rerun()

st.title("MacroLens: Regime-Based Portfolio Strategy")
st.write(
    "This dashboard shows the backtest results of a macro regime-based sector "
    "allocation strategy plus a near-live ETF market snapshot."
)
st.caption("Live market data refreshes every 5 minutes.")

# Load core results
results = pd.read_csv("results/backtest_results.csv", index_col=0, parse_dates=True)

summary = pd.read_csv("results/performance_summary.csv", index_col=0, header=None)
summary.columns = ["Value"]
summary = summary.iloc[1:].copy()
summary.index = summary.index.astype(str)
summary.index.name = "Metric"

weights_history = pd.read_csv("results/weights_history.csv", index_col=0, parse_dates=True)

# Load Monte Carlo results
mc_summary = pd.read_csv("results/monte_carlo_summary.csv", index_col=0, header=None)
mc_summary.columns = ["Value"]
mc_summary = mc_summary.iloc[1:].copy()
mc_summary.index = mc_summary.index.astype(str)
mc_summary.index.name = "Metric"

portfolio_paths = pd.read_csv("results/portfolio_simulation_paths.csv", index_col=0)
benchmark_paths = pd.read_csv("results/benchmark_simulation_paths.csv", index_col=0)

# Live snapshot
live_df = load_live_snapshot()

st.subheader("Live Market Snapshot")
if not live_df.empty:
    display_live = live_df.copy()
    display_live["Latest Price"] = display_live["Latest Price"].map(lambda x: round(x, 2))
    display_live["Previous Close"] = display_live["Previous Close"].map(lambda x: round(x, 2))
    display_live["Daily Return"] = display_live["Daily Return"].map(lambda x: f"{x:.2%}")
    st.dataframe(display_live, use_container_width=True)

    benchmark_row = live_df[live_df["Ticker"] == BENCHMARK]
    sector_only = live_df[live_df["Ticker"] != BENCHMARK].copy()

    col1, col2, col3 = st.columns(3)

    with col1:
        if not benchmark_row.empty:
            spy_price = benchmark_row["Latest Price"].iloc[0]
            spy_move = benchmark_row["Daily Return"].iloc[0]
            st.metric("SPY Live Price", f"{spy_price:.2f}", f"{spy_move:.2%}")

    with col2:
        if not sector_only.empty:
            best_sector = sector_only.sort_values("Daily Return", ascending=False).iloc[0]
            st.metric(
                "Strongest Sector Today",
                best_sector["Ticker"],
                f"{best_sector['Daily Return']:.2%}"
            )

    with col3:
        if not sector_only.empty:
            worst_sector = sector_only.sort_values("Daily Return", ascending=True).iloc[0]
            st.metric(
                "Weakest Sector Today",
                worst_sector["Ticker"],
                f"{worst_sector['Daily Return']:.2%}"
            )
else:
    st.warning("Live market snapshot could not be loaded.")

# Performance summary
st.subheader("Performance Summary")
st.dataframe(summary, use_container_width=True)

# Current regime
st.subheader("Current Market Regime")
current_regime = results["regime"].iloc[-1]

if current_regime == "Growth":
    st.success(f"Latest detected regime: {current_regime}")
elif current_regime == "Inflationary":
    st.warning(f"Latest detected regime: {current_regime}")
elif current_regime == "Defensive":
    st.error(f"Latest detected regime: {current_regime}")
else:
    st.info(f"Latest detected regime: {current_regime}")

# Current weights
st.subheader("Current Portfolio Weights")
current_weights = weights_history.iloc[-1].sort_values(ascending=False)
positive_weights = current_weights[current_weights > 0]
st.dataframe(positive_weights, use_container_width=True)

# Top sector tilts
st.subheader("Top Sector Tilts")
top_3 = positive_weights.head(3)
tilt_text = ", ".join([f"{ticker} ({weight:.1%})" for ticker, weight in top_3.items()])
st.write(f"**Top sector exposures:** {tilt_text}")

# Model-implied move
st.subheader("Model-Implied Portfolio Move Today")
if not live_df.empty:
    live_returns = live_df.set_index("Ticker")["Daily Return"].to_dict()

    implied_move = 0.0
    for ticker, weight in current_weights.items():
        if ticker in live_returns:
            implied_move += weight * live_returns[ticker]

    benchmark_live_return = live_returns.get(BENCHMARK, 0.0)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Model-Implied Portfolio Return Today", f"{implied_move:.2%}")
    with col2:
        st.metric("SPY Return Today", f"{benchmark_live_return:.2%}")

# Monte Carlo summary
st.subheader("Monte Carlo Probability Summary")
st.dataframe(mc_summary, use_container_width=True)

# Monte Carlo portfolio paths
st.subheader("Monte Carlo Simulated Portfolio Paths")
sample_portfolio_paths = portfolio_paths.iloc[:, :100]
st.line_chart(sample_portfolio_paths)

# Monte Carlo benchmark paths
st.subheader("Monte Carlo Simulated Benchmark Paths")
sample_benchmark_paths = benchmark_paths.iloc[:, :100]
st.line_chart(sample_benchmark_paths)

# Growth chart
st.subheader("Growth of $1")
st.line_chart(results[["portfolio_growth", "benchmark_growth"]])

# Drawdown chart
st.subheader("Drawdown")
drawdown_df = pd.DataFrame(index=results.index)
drawdown_df["portfolio_drawdown"] = (
    results["portfolio_growth"] - results["portfolio_growth"].cummax()
) / results["portfolio_growth"].cummax()

drawdown_df["benchmark_drawdown"] = (
    results["benchmark_growth"] - results["benchmark_growth"].cummax()
) / results["benchmark_growth"].cummax()

st.line_chart(drawdown_df)

# Rolling Sharpe
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

st.line_chart(rolling_sharpe)

# Rolling volatility
st.subheader("Rolling 12-Month Volatility")
rolling_vol = pd.DataFrame(index=results.index)

rolling_vol["portfolio_rolling_volatility"] = (
    results["portfolio_return"].rolling(12).std()
) * (12 ** 0.5)

rolling_vol["benchmark_rolling_volatility"] = (
    results["benchmark_return"].rolling(12).std()
) * (12 ** 0.5)

st.line_chart(rolling_vol)

# Monthly returns
st.subheader("Monthly Returns")
st.line_chart(results[["portfolio_return", "benchmark_return"]])

# Regime distribution
st.subheader("Regime Distribution")
regime_counts = results["regime"].value_counts()
st.bar_chart(regime_counts)

# Recent data
st.subheader("Recent Backtest Data")
st.dataframe(results.tail(20), use_container_width=True)