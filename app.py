import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from bot import get_candles, strategy  # Your files
from indicators import compute_indicators
import time

st.set_page_config(layout="wide", page_title="Crypto Stock Analyzer")

# Sidebar
with st.sidebar:
    symbol = st.text_input("Symbol", value="BTCUSDT")
    interval = st.selectbox("Interval", ["5m", "1h", "1d"])
    if st.button("Run Strategy"):
        st.cache_data.clear()
        st.rerun()

# Fetch & Display Data
@st.cache_data(ttl=60)
def load_data():
    candles = get_candles(symbol, interval, 100)
    df = compute_indicators(candles)
    return df

df = load_data()

# Header Metrics
col1, col2, col3 = st.columns(3)
latest = df.iloc[-1]
col1.metric("Price", f"${latest['close']:.2f}")
col2.metric("RSI", f"{latest['rsi']:.1f}")
col3.metric("EMA12/26", f"{latest['ema12']:.2f}/{latest['ema26']:.2f}")

# Charts Tab
tab1, tab2 = st.tabs(["Candles", "Signals"])
with tab1:
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close']
    ))
    fig.add_trace(go.Scatter(x=df['time'], y=df['ema12'], name="EMA12"))
    fig.add_trace(go.Scatter(x=df['time'], y=df['ema26'], name="EMA26"))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    signal = strategy()  # Runs your logic, prints BUY/SELL/No trade
    st.write("Latest Signal:", signal)
