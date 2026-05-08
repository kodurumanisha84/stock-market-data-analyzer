import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Stock Market Data Analyzer",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("📈 Stock Market Data Analyzer")
st.markdown("### Interactive Financial Analytics Dashboard")

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("Dashboard Controls")

stock_options = [
    "AAPL",
    "TSLA",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NFLX",
    "NVDA",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]

ticker = st.sidebar.selectbox(
    "Select Company",
    stock_options
)

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2020-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("today")
)

# -----------------------------------
# FETCH DATA
# -----------------------------------

@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data

df = load_data(ticker, start_date, end_date)

# -----------------------------------
# HANDLE EMPTY DATA
# -----------------------------------

if df.empty:
    st.error("No data found for selected ticker.")
    st.stop()

# -----------------------------------
# CALCULATIONS
# -----------------------------------

df["Daily Return"] = df["Close"].pct_change()

df["SMA20"] = df["Close"].rolling(window=20).mean()
df["SMA50"] = df["Close"].rolling(window=50).mean()

volatility = df["Daily Return"].std()

latest_close = df["Close"].iloc[-1]
highest_price = df["High"].max()
lowest_price = df["Low"].min()

# -----------------------------------
# KPI METRICS
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Latest Close", f"${latest_close:.2f}")

col2.metric("Highest Price", f"${highest_price:.2f}")

col3.metric("Lowest Price", f"${lowest_price:.2f}")

col4.metric("Volatility", f"{volatility:.4f}")

# -----------------------------------
# CANDLESTICK CHART
# -----------------------------------

st.subheader("📊 Candlestick Chart")

fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"]
)])

fig.update_layout(
    height=600,
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# MOVING AVERAGES
# -----------------------------------

st.subheader("📈 Moving Average Analysis")

ma_fig = go.Figure()

ma_fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Close"],
    mode='lines',
    name='Close Price'
))

ma_fig.add_trace(go.Scatter(
    x=df.index,
    y=df["SMA20"],
    mode='lines',
    name='SMA20'
))

ma_fig.add_trace(go.Scatter(
    x=df.index,
    y=df["SMA50"],
    mode='lines',
    name='SMA50'
))

ma_fig.update_layout(
    height=500,
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(ma_fig, use_container_width=True)

# -----------------------------------
# VOLUME CHART
# -----------------------------------

st.subheader("📦 Trading Volume")

volume_fig = px.bar(
    df,
    x=df.index,
    y="Volume"
)

volume_fig.update_layout(height=400)

st.plotly_chart(volume_fig, use_container_width=True)

# -----------------------------------
# DAILY RETURN DISTRIBUTION
# -----------------------------------

st.subheader("📉 Daily Return Distribution")

hist_fig = px.histogram(
    df,
    x="Daily Return",
    nbins=50
)

hist_fig.update_layout(height=400)

st.plotly_chart(hist_fig, use_container_width=True)

# -----------------------------------
# DATA PREVIEW
# -----------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(df.tail())

# -----------------------------------
# DOWNLOAD BUTTON
# -----------------------------------

csv = df.to_csv().encode('utf-8')

st.download_button(
    label="⬇ Download Dataset",
    data=csv,
    file_name=f"{ticker}_stock_data.csv",
    mime="text/csv"
)

# -----------------------------------
# FINAL INSIGHTS
# -----------------------------------

st.subheader("🧠 Financial Insights")

if latest_close > df["SMA20"].iloc[-1]:
    st.success("Stock is trading above SMA20 → Short-term bullish trend.")

if latest_close > df["SMA50"].iloc[-1]:
    st.success("Stock is trading above SMA50 → Long-term bullish trend.")

if volatility > 0.03:
    st.warning("High volatility detected → Higher investment risk.")

else:
    st.info("Moderate volatility detected.")

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")
st.caption("Educational Project Only — Not Financial Advice")