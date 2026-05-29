import streamlit as st
import pandas as pd
import numpy as np
from data_fetcher import fetch_gold_data, fetch_latest_price
from macd_strategy import calculate_macd, generate_signals
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Gold Trading Bot - MACD Strategy",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Gold Trading Bot - MACD Strategy")
st.markdown("""
This bot displays live gold price data, calculates MACD indicators, and generates buy/sell signals.
**Note:** This is for educational purposes only. Not financial advice.
""")

# Sidebar controls
st.sidebar.header("Settings")
data_period = st.sidebar.selectbox(
    "Data Period",
    options=["15m", "30m", "1h", "4h", "1d"],
    index=2
)
data_interval = st.sidebar.selectbox(
    "Data Interval",
    options=["1m", "5m", "15m", "30m", "1h"],
    index=1
)
refresh_interval = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=5,
    max_value=60,
    value=10
)

# Auto-refresh component
count = st_autorefresh(
    interval=refresh_interval * 1000,  # in milliseconds
    key="golddatarefresh"
)

# Placeholder for data
placeholder = st.empty()

# Fetch data
try:
    with st.spinner("Fetching gold price data..."):
        data = fetch_gold_data(period=data_period, interval=data_interval)

    if data.empty:
        st.error("No data fetched. Please check your internet connection or try different settings.")
    else:
        # Calculate MACD
        macd_data = calculate_macd(data['Close'])
        signals = generate_signals(macd_data)

        # Add MACD and signals to dataframe
        data['MACD_line'] = macd_data['macd']
        data['Signal_line'] = macd_data['signal']
        data['MACD_hist'] = macd_data['histogram']
        data['Signal'] = signals  # 1 for buy, -1 for sell, 0 for hold

        # Latest price
        latest_price = data['Close'].iloc[-1]
        latest_time = data.index[-1]

        # Display latest price
        placeholder.metric(
            label="Latest Gold Price (GC=F)",
            value=f"${latest_price:.2f}",
            delta=f"{(data['Close'].iloc[-1] - data['Close'].iloc[-2]):.2f}" if len(data) > 1 else "0.00"
        )

        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Price Chart", "MACD Indicator", "Signals"])

        with tab1:
            st.subheader("Gold Price Chart")
            st.line_chart(data['Close'])

        with tab2:
            st.subheader("MACD Indicator")
            macd_chart_data = data[['MACD_line', 'Signal_line']]
            st.line_chart(macd_chart_data)
            st.subheader("MACD Histogram")
            st.bar_chart(data['MACD_hist'])

        with tab3:
            st.subheader("Buy/Sell Signals")
            # Display latest signal
            latest_signal = data['Signal'].iloc[-1]
            if latest_signal == 1:
                st.success("🟢 BUY Signal")
            elif latest_signal == -1:
                st.error("🔴 SELL Signal")
            else:
                st.info("⚪ HOLD")

            # Show recent signals
            st.subheader("Recent Signals")
            recent_signals = data[data['Signal'] != 0].tail(10)
            if not recent_signals.empty:
                st.dataframe(recent_signals[['Close', 'Signal']])
            else:
                st.write("No signals in the selected period.")

        # Show raw data (optional)
        if st.checkbox("Show raw data"):
            st.subheader("Raw Data")
            st.dataframe(data)

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    st.info("Try adjusting the period or interval, or check your internet connection.")

# Add a button to manually refresh
if st.button("Refresh Now"):
    st.rerun()