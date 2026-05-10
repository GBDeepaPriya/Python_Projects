import sys
import os

# ---------------------------------------------------
# FIX IMPORTS
# ---------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# ---------------------------------------------------
# IMPORTS
# ---------------------------------------------------

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.ingest import upsert_daily
from src.indicators import compute_indicators
from src.backtest import run_backtest

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

DB = "db/market.db"

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Advanced Stock Market Analyzer",
    layout="wide"
)

st.title("📈Stock Market Dashboard")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("⚙ Dashboard Settings")

available_stocks = [
    "AAPL", "MSFT", "TSLA", "NVDA",
    "GOOGL", "AMZN", "META", "NFLX"
]

selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    available_stocks,
    default=["AAPL", "TSLA", "NVDA", "NFLX"]
)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Line", "Candlestick", "Area"]
)

show_sma = st.sidebar.checkbox(
    "Show SMA20 / SMA50",
    value=True
)

days = st.sidebar.slider(
    "Historical Days",
    30,
    1000,
    252
)

# ---------------------------------------------------
# LOAD DATA BUTTON
# ---------------------------------------------------

st.sidebar.subheader("📡 Market Data Loader")

if st.sidebar.button("Load Market Data"):

    progress_bar = st.progress(0)
    status = st.empty()

    success, failed = [], []

    for i, ticker in enumerate(selected_stocks):

        try:
            status.info(f"Fetching {ticker}...")

            upsert_daily(ticker)
            compute_indicators(ticker)

            success.append(ticker)

        except Exception as e:
            failed.append(f"{ticker}: {str(e)}")

        progress_bar.progress((i + 1) / len(selected_stocks))

    status.empty()

    if success:
        st.success(f"Loaded: {', '.join(success)}")

    if failed:
        st.error("\n".join(failed))

# ---------------------------------------------------
# DB CONNECTION
# ---------------------------------------------------

con = sqlite3.connect(DB)
all_data = []

# ---------------------------------------------------
# LOAD STOCK DATA
# ---------------------------------------------------

for ticker in selected_stocks:

    try:

        query = """
        SELECT c.date,
               c.open,
               c.high,
               c.low,
               c.close,
               c.volume,
               i.sma20,
               i.sma50,
               i.rsi14
        FROM candles_daily c
        LEFT JOIN (
            SELECT DISTINCT ticker, date, sma20, sma50, rsi14
            FROM indicators_daily
        ) i
        ON c.ticker=i.ticker
        AND c.date=i.date
        WHERE c.ticker=?
        ORDER BY c.date ASC
        LIMIT CAST(? AS INTEGER)
        """

        df = pd.read_sql_query(query, con, params=[ticker, days])

        if df.empty:
            st.warning(f"No data found for {ticker}")
            continue

        df["ticker"] = ticker
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        all_data.append(df)

    except Exception as e:
        st.error(f"{ticker} Load Error: {e}")

con.close()

# ---------------------------------------------------
# MAIN UI
# ---------------------------------------------------

if len(all_data) > 0:

    combined_df = pd.concat(all_data)
    combined_df = combined_df.sort_values(["ticker", "date"])

    # ---------------------------------------------------
    # SAFE PIVOT (FIXED)
    # ---------------------------------------------------

    price_pivot = combined_df.pivot_table(
        index="date",
        columns="ticker",
        values="close"
    )

    price_pivot = price_pivot.sort_index()

    # ONLY forward fill (NO bfill)
    price_pivot = price_pivot.ffill()

    # drop rows where ALL are NaN
    price_pivot = price_pivot.dropna(how="all")

    # ---------------------------------------------------
    # RETURNS
    # ---------------------------------------------------

    returns_df = price_pivot.pct_change().dropna()

    # ---------------------------------------------------
    # MARKET SUMMARY
    # ---------------------------------------------------

    st.subheader("📌 Market Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Stocks Selected", len(selected_stocks))
    col2.metric("Total Records", len(combined_df))
    col3.metric("Avg Close Price", round(combined_df["close"].mean(), 2))

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Performance",
        "📊 Individual Charts",
        "🧠 Technical Analysis",
        "💰 Backtest",
        "📋 Raw Data"
    ])

    # ===================================================
    # TAB 1 - PERFORMANCE
    # ===================================================

    with tab1:

        st.subheader("📈 Multi-Stock Comparison")

        compare_mode = st.radio(
            "Comparison Mode",
            ["Actual Prices", "Percentage Growth"],
            horizontal=True
        )

        chart_df = price_pivot.copy()

        # ---------------------------------------------------
        # FIX: PROPER NORMALIZATION (IMPORTANT)
        # ---------------------------------------------------

        if compare_mode == "Percentage Growth":

            chart_df = chart_df / chart_df.iloc[0] * 100

        # ---------------------------------------------------
        # PLOT
        # ---------------------------------------------------

        fig_compare = go.Figure()

        stock_colors = {
            "AAPL": "#00CC96",
            "TSLA": "#EF553B",
            "NVDA": "#AB63FA",
            "NFLX": "#FFA15A",
            "AMZN": "#19D3F3",
            "MSFT": "#636EFA",
            "META": "#FF6692",
            "GOOGL": "#B6E880"
        }

        for ticker in chart_df.columns:

            fig_compare.add_trace(
                go.Scatter(
                    x=chart_df.index,
                    y=chart_df[ticker],
                    mode="lines",
                    name=ticker,
                    line=dict(
                        width=3,
                        color=stock_colors.get(ticker)
                    )
                )
            )

        fig_compare.update_layout(
            template="plotly_dark",
            height=700,
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Growth %" if compare_mode == "Percentage Growth" else "Price"
        )

        st.plotly_chart(fig_compare, use_container_width=True)

        # ---------------------------------------------------
        # RETURNS DISTRIBUTION
        # ---------------------------------------------------

        st.subheader("📦 Daily Returns")

        returns_long = returns_df.melt(
            var_name="Ticker",
            value_name="Return"
        )

        fig_box = px.box(
            returns_long,
            x="Ticker",
            y="Return",
            color="Ticker"
        )

        fig_box.update_layout(template="plotly_dark", height=500)

        st.plotly_chart(fig_box, use_container_width=True)

    # ===================================================
    # TAB 2 - INDIVIDUAL CHARTS
    # ===================================================

    with tab2:

        stock = st.selectbox("Choose Stock", selected_stocks)

        df = combined_df[combined_df["ticker"] == stock]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["close"],
            mode="lines",
            name="Close"
        ))

        if show_sma:
            fig.add_trace(go.Scatter(x=df["date"], y=df["sma20"], name="SMA20"))
            fig.add_trace(go.Scatter(x=df["date"], y=df["sma50"], name="SMA50"))

        fig.update_layout(template="plotly_dark", height=600)

        st.plotly_chart(fig, use_container_width=True)

    # ===================================================
    # TAB 3 - TECHNICAL
    # ===================================================

    with tab3:

        tech = st.selectbox("Stock", selected_stocks, key="tech")

        df = combined_df[combined_df["ticker"] == tech]

        st.plotly_chart(px.line(df, x="date", y="rsi14",
                                title="RSI").update_layout(template="plotly_dark"),
                        use_container_width=True)

        st.plotly_chart(px.bar(df, x="date", y="volume",
                               title="Volume").update_layout(template="plotly_dark"),
                        use_container_width=True)

    # ===================================================
    # TAB 4 - BACKTEST
    # ===================================================

    with tab4:

        metrics = []

        for ticker in selected_stocks:

            try:
                stats = run_backtest(ticker)

                metrics.append({
                    "Ticker": ticker,
                    "Return": stats["Total Return"],
                    "Sharpe": stats["Sharpe Ratio"],
                    "Drawdown": stats["Max Drawdown"]
                })

            except Exception as e:
                st.warning(f"{ticker}: {e}")

        dfm = pd.DataFrame(metrics)

        st.dataframe(dfm, use_container_width=True)

    # ===================================================
    # TAB 5
    # ===================================================

    with tab5:

        st.dataframe(combined_df, use_container_width=True)

        st.download_button(
            "Download CSV",
            combined_df.to_csv(index=False),
            file_name="stocks.csv"
        )

else:
    st.warning("Load market data first.")