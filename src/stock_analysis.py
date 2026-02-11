# src/stock_analysis.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io


def normalize_symbol(symbol):
    """
    Normalize stock symbol.
    Example:
    - reliance -> RELIANCE.NS
    - AAPL -> AAPL
    """
    symbol = symbol.upper().strip()

    # If user enters Indian stock without .NS, add it
    if "." not in symbol and symbol not in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]:
        symbol = symbol + ".NS"

    return symbol


def get_stock_data(symbol, period="5y", interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance.

    symbol: 'AAPL', 'RELIANCE.NS'
    period: '1mo', '6mo', '1y', '5y', 'max'
    interval: '1d', '1wk', '1mo'

    Returns: pandas DataFrame
    """
    try:
        symbol = normalize_symbol(symbol)
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)

        if data.empty:
            return pd.DataFrame()

        return data

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()


def plot_stock_chart(data, symbol):
    """
    Plot closing price chart and return image buffer for Streamlit.
    """
    if data.empty:
        return None

    plt.figure(figsize=(12, 5))
    plt.plot(data.index, data["Close"], label="Close Price", linewidth=2)

    plt.title(f"{symbol} – Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()

    # Save plot to memory buffer (Streamlit friendly)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()

    return buf
