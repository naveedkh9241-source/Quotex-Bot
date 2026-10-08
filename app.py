import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

st.set_page_config(page_title="Quotex Live Bot", page_icon="📈")

dubai_tz = pytz.timezone('Asia/Dubai')
now = datetime.now(dubai_tz)
st.success(f"📍 Sharjah Area 6 | 🕒 Dubai Live: {now.strftime('%H:%M:%S')}")

st.title("Quotex Live Bot - Naveed")
st.caption("LIVE BUY/SELL - 1 Minute")

pair = st.selectbox("Pair Select Karo:", ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "BTC/USD"])
map_dict = {"EUR/USD":"EURUSD=X", "GBP/USD":"GBPUSD=X", "USD/JPY":"JPY=X", "AUD/USD":"AUDUSD=X", "BTC/USD":"BTC-USD"}
symbol = map_dict[pair]

@st.cache_data(ttl=30)
def get_data(sym):
    df = yf.download(sym, period="1d", interval="1m")
    return df

df = get_data(symbol)
price = float(df['Close'].iloc[-1])

delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))
rsi_val = float(rsi.iloc[-1])

st.metric(f"{pair} Price", f"{price:.5f}", f"RSI {rsi_val:.1f}")

if rsi_val >= 50:
    st.markdown(f"<div style='background:#22c55e;padding:30px;border-radius:20px;text-align:center;color:white'><h1>🟢 BUY - {pair}</h1><h3>NEXT 1 MIN UP</h3></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='background:#ef4444;padding:30px;border-radius:20px;text-align:center;color:white'><h1>🔴 SELL - {pair}</h1><h3>NEXT 1 MIN DOWN</h3></div>", unsafe_allow_html=True)

st.dataframe(df.tail(5))
