import pandas as pd
import numpy as np

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Calculate MACD, signal line, and histogram.

    Args:
        prices (pd.Series): Series of closing prices
        fast (int): Fast EMA period
        slow (int): Slow EMA period
        signal (int): Signal line EMA period

    Returns:
        dict: Contains 'macd', 'signal', 'histogram' as pd.Series
    """
    # Calculate EMAs
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()

    # MACD line
    macd = ema_fast - ema_slow

    # Signal line
    signal_line = macd.ewm(span=signal, adjust=False).mean()

    # Histogram
    histogram = macd - signal_line

    return {
        'macd': macd,
        'signal': signal_line,
        'histogram': histogram
    }

def generate_signals(macd_data):
    """
    Generate buy/sell signals based on MACD crossovers.

    Args:
        macd_data (dict): Output from calculate_macd

    Returns:
        pd.Series: Series with values 1 (buy), -1 (sell), 0 (hold)
    """
    macd = macd_data['macd']
    signal = macd_data['signal']

    # Initialize signals
    signals = pd.Series(0, index=macd.index)

    # Buy signal: MACD crosses above signal line
    buy_condition = (macd > signal) & (macd.shift(1) <= signal.shift(1))
    signals[buy_condition] = 1

    # Sell signal: MACD crosses below signal line
    sell_condition = (macd < signal) & (macd.shift(1) >= signal.shift(1))
    signals[sell_condition] = -1

    return signals