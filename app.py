import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

st.title("🇮🇳 Indian Stock Market Dashboard")

# stock selection
stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "SBI": "SBIN.NS",
    "ITC": "ITC.NS"
}

selected_stock = st.selectbox("Select Stock", list(stocks.keys()))
ticker = stocks[selected_stock]

# period filter
period = st.selectbox("Select Period", ["1d", "5d", "1mo", "6mo", "1y"])

# caching
@st.cache_data(ttl=60)
def load_data(ticker, period):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval="1d")

data = load_data(ticker, period)

# KPIs
col1, col2, col3 = st.columns(3)

latest = data["Close"].iloc[-1]
prev = data["Close"].iloc[-2]

col1.metric("Current Price ₹", round(latest, 2), round(latest - prev, 2))
col2.metric("High ₹", round(data["High"].max(), 2))
col3.metric("Low ₹", round(data["Low"].min(), 2))

st.markdown("---")

# chart
st.subheader("📈 Price Trend")
st.line_chart(data["Close"])

# volume chart
st.subheader("📊 Volume")
st.bar_chart(data["Volume"])

# data table
st.subheader("📋 Recent Data")
st.dataframe(data.tail(10))
