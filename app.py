import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="Quotex Bot - Naveed", layout="centered")
tz = pytz.timezone('Asia/Dubai')
now = datetime.now(tz)
st.success(f"📍 Sharjah Area 6 | 🕒 Dubai: {now.strftime('%H:%M:%S')}")

st.title("📈 Quotex Live Bot - Naveed")
st.caption("LIVE BUY/SELL - 1 Minute")

pair = st.selectbox("Pair Select Karo:", ["EUR/USD","GBP/USD","USD/JPY","AUD/USD","BTC/USD"])
mp = {"EUR/USD":"EURUSD=X","GBP/USD":"GBPUSD=X","USD/JPY":"JPY=X","AUD/USD":"AUDUSD=X","BTC/USD":"BTC-USD"}

@st.cache_data(ttl=30)
def get_df(sym):
    return yf.download(sym, period="1d", interval="1m", progress=False, auto_adjust=True)

df = get_df(mp[pair])

close_col = df['Close']
if isinstance(close_col, pd.DataFrame):
    close_col = close_col.iloc[:,0]

price = float(close_col.iloc[-1])

rsi_val = 50.0
try:
    delta = close_col.diff()
    gain = delta.where(delta>0,0).rolling(14).mean()
    loss = -delta.where(delta<0,0).rolling(14).mean()
    rs = gain/loss
    rsi = 100-(100/(1+rs))
    rsi_val = float(rsi.iloc[-1])
except:
    pass

st.metric(pair, f"{price:.5f}", f"RSI {rsi_val:.1f}")

if rsi_val >= 50:
    st.markdown(f"<div style='background:#22c55e;padding:35px;border-radius:20px;text-align:center;color:white'><h1>🟢 BUY - {pair}</h1><h2>NEXT 1 MIN UP ⬆️</h2><p>RSI: {rsi_val:.1f}</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='background:#ef4444;padding:35px;border-radius:20px;text-align:center;color:white'><h1>🔴 SELL - {pair}</h1><h2>NEXT 1 MIN DOWN ⬇️</h2><p>RSI: {rsi_val:.1f}</p></div>", unsafe_allow_html=True)

st.line_chart(close_col.tail(60))

if st.button("🔄 Refresh Signal"):
    st.cache_data.clear()
    st.rerun()
