import yfinance as yf
import pandas as pd

stock_prices = yf.download(tickers = "GME", start = "2020-01-01", end = "2021-10-26")

stock_prices.to_excel("data/stock_prices.xlsx")

