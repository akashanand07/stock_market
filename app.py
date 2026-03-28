import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("🇮🇳 Indian Stock Market PRO Dashboard")

# Stock list
stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "SBI": "SBIN.NS",
    "ITC": "ITC.NS"
}

# Sidebar
st.sidebar.header("Filters")
selected_stock = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo", "6mo", "1y"])

ticker = stocks[selected_stock]

# Load data
@st.cache_data(ttl=60)
def load_data(ticker, period):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval="1d")

data = load_data(ticker, period)

# Handle empty data
if data.empty:
    st.warning("No data available. Try different stock or time.")
    st.stop()

# ================= KPI =================
col1, col2, col3 = st.columns(3)

latest = data["Close"].iloc[-1]

if len(data) > 1:
    prev = data["Close"].iloc[-2]
    change = latest - prev
else:
    change = 0

col1.metric("Current Price ₹", round(latest, 2), round(change, 2))
col2.metric("High ₹", round(data["High"].max(), 2))
col3.metric("Low ₹", round(data["Low"].min(), 2))

st.markdown("---")

# ================= MOVING AVERAGE =================
data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()

# ================= BUY/SELL SIGNAL =================
data["Signal"] = 0
data.loc[data["MA20"] > data["MA50"], "Signal"] = 1
data.loc[data["MA20"] < data["MA50"], "Signal"] = -1

last_signal = data["Signal"].iloc[-1]

if last_signal == 1:
    st.success("🟢 BUY Signal (MA20 > MA50)")
elif last_signal == -1:
    st.error("🔴 SELL Signal (MA20 < MA50)")
else:
    st.info("⚪ HOLD")

# ================= CANDLESTICK =================
st.subheader("📊 Candlestick Chart")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Price"
))

# Moving averages
fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA20"],
    line=dict(color="blue", width=1),
    name="MA20"
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA50"],
    line=dict(color="orange", width=1),
    name="MA50"
))

st.plotly_chart(fig, use_container_width=True)

# ================= VOLUME =================
st.subheader("📊 Volume")
st.bar_chart(data["Volume"])

# ================= TABLE =================
st.subheader("📋 Recent Data")
st.dataframe(data.tail(10))
