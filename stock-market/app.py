import yfinance as yf
import pandas as pd
import time

while True:
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1d", interval="1m")

    data.to_csv("stock_data.csv")

    print("Updated")

    time.sleep(30)
