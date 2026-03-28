import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Live Stock Dashboard")

# user input
ticker = st.text_input("Enter Stock Symbol", "AAPL")

# caching to avoid rate limit
@st.cache_data(ttl=60)
def load_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")
    return data

# load data
data = load_data(ticker)

# display
st.write(data)
st.line_chart(data["Close"])
