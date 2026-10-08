import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
import requests
from datetime import datetime

st.set_page_config(page_title="Quotex King Bot - Dubai", page_icon="👑", layout="centered")
DUBAI_TZ = pytz.timezone('Asia/Dubai')

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=10)
        return True
    except:
        return False

st.title("👑 Quotex King Bot - Dubai Time")
st.markdown(f"**Dubai Time:** {datetime.now(DUBAI_TZ).strftime('%Y-%m-%d %I:%M:%S %p')}")
st.sidebar.header("⚙️ Settings")
pair = st.sidebar.selectbox("Pair", ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY", "Gold (XAU/USD)", "BTC-USD"])
symbol_map = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X", "AUD/USD": "AUDUSD=X", "USD/CAD": "CAD=X", "EUR/JPY": "EURJPY=X", "GBP/JPY": "GBPJPY=X", "Gold (XAU/USD)": "GC=F", "BTC-USD": "BTC-USD"}
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m"], index=1)
st.divider()

yf_symbol = symbol_map.get(pair, "EURUSD=X")
interval = "1m" if timeframe=="1m" else "5m" if timeframe=="5m" else "15m"

with st.spinner(f"{pair} ka data..."):
    df = yf.download(yf_symbol, period="1d", interval=interval, progress=False)
    if df.empty:
        st.error("Data nahi mil raha!")
        st.stop()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    last_close = float(df['Close'].iloc[-1])
    last_ma20 = float(df['MA20'].iloc[-1])
    last_ma50 = float(df['MA50'].iloc[-1])
    signal = "WAIT"
    confidence = 75
    if last_close > last_ma20 and last_ma20 > last_ma50:
        signal = "BUY 🟢"
        confidence = 88
    elif last_close < last_ma20 and last_ma20 < last_ma50:
        signal = "SELL 🔴"
        confidence = 86
    c1,c2 = st.columns(2)
    c1.metric(f"{pair} Price", f"{last_close:.5f}")
    c2.metric("Signal", signal)
    st.line_chart(df['Close'].tail(100))
    st.subheader(f"Signal: {signal} | Confidence: {confidence}%")
    if signal != "WAIT":
        msg = f"👑 *Quotex King Signal*\n\nPair: {pair}\nSignal: {signal}\nPrice: {last_close}\nConfidence: {confidence}%\nTime: {datetime.now(DUBAI_TZ).strftime('%I:%M %p')} Dubai"
        if st.button("📤 Telegram Pe Bhejo"):
            if send_telegram(msg):
                st.success("Telegram pe bhej diya! ✅")
                st.balloons()
            else:
                st.error("Token/ID galat hai!")
