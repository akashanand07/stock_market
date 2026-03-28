import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Indian Stock Dashboard", layout="wide")

st.title("📈 Indian Stock Market Dashboard (Pro)")

# =========================
# 📊 STOCK SELECTION
# =========================
stocks = {
    "TCS": "TCS.NS",
    "Reliance": "RELIANCE.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Wipro": "WIPRO.NS",
    "SBI": "SBIN.NS"
}

selected_stock = st.selectbox("Select Stock", list(stocks.keys()))
ticker = stocks[selected_stock]

period = st.selectbox("Select Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])

# =========================
# 📥 FETCH DATA
# =========================
data = yf.download(ticker, period=period, interval="1m")

# =========================
# ❌ ERROR HANDLING
# =========================
if data.empty:
    st.error("No data found. Try another stock or period.")
    st.stop()

# =========================
# 📊 KPI METRICS
# =========================
if len(data) >= 2:
    latest = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2]
    change = latest - prev
    percent = (change / prev) * 100

    col1, col2 = st.columns(2)

    col1.metric("Current Price", f"₹ {latest:.2f}")
    col2.metric("Change", f"{change:.2f}", f"{percent:.2f}%")
else:
    st.warning("Not enough data for metrics")

# =========================
# 📉 MOVING AVERAGE (BUY/SELL)
# =========================
data["MA20"] = data["Close"].rolling(window=20).mean()

# =========================
# 🕯️ CANDLESTICK CHART
# =========================
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Candlestick"
))

# Moving Average line
fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA20"],
    line=dict(color='blue', width=2),
    name="MA20"
))

fig.update_layout(
    title=f"{selected_stock} Price Chart",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 📊 BUY / SELL SIGNAL
# =========================
st.subheader("📢 Trading Signal")

if len(data) >= 20:
    if data["Close"].iloc[-1] > data["MA20"].iloc[-1]:
        st.success("🟢 BUY Signal (Price above MA20)")
    else:
        st.error("🔴 SELL Signal (Price below MA20)")
else:
    st.warning("Not enough data for signals")

# =========================
# 📋 DATA TABLE
# =========================
st.subheader("📄 Raw Data")
st.dataframe(data.tail(10))
