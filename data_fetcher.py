import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_gold_data(period="1d", interval="5m"):
    """
    Fetch recent gold price data using yfinance.

    Args:
        period (str): Data period (e.g., "1d", "5d", "1mo")
        interval (str): Data interval (e.g., "1m", "5m", "15m", "1h", "1d")

    Returns:
        pd.DataFrame: DataFrame with OHLCV data
    """
    # Gold futures ticker
    ticker = "GC=F"
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    if data.empty:
        # Fallback to spot gold ticker
        ticker = "XAUUSD=X"
        data = yf.download(ticker, period=period, interval=interval, progress=False)
    return data

def fetch_latest_price():
    """
    Fetch the latest gold price.

    Returns:
        float: Latest closing price
    """
    data = fetch_gold_data(period="1d", interval="1m")
    if not data.empty:
        return data['Close'].iloc[-1]
    else:
        raise ValueError("Could not fetch gold price data")