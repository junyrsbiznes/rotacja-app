import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Hard Assets Ratio Advisor", layout="wide")

st.title("🪙 Hard Assets Ratio Advisor")

# --- USTAWIENIA PROGÓW ---
# Zgodnie z prośbą: GSR wymiana przy 60, BTC/Gold 15/40
gsr_limit = 60
btc_gold_low = 15
btc_gold_high = 40

@st.cache_data(ttl=3600)
def load_data():
    tickers = {'Gold': 'GC=F', 'Silver': 'SI=F', 'BTC': 'BTC-USD'}
    df = pd.DataFrame()
    for name, ticker in tickers.items():
        data = yf.download(ticker, period="5y")
        if not data.empty:
            df[name] = data['Close'].squeeze()
    return df.ffill().dropna()

data = load_data()
data['GSR'] = data['Gold'] / data['Silver']
data['BTC_Gold'] = data['BTC'] / data['Gold']

# Ostatnie wartości
curr_gsr = data['GSR'].iloc[-1]
curr_btc_gold = data['BTC_Gold'].iloc[-1]

# --- WIDGETY I SYGNAŁY ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Strategia Metali (GSR)")
    st.metric("Aktualne GSR", f"{curr_gsr:.2f}")
    if curr_gsr >= gsr_limit:
        st.success(f"📈 Sygnał: KUPUJ SREBRO (GSR >= {gsr_limit})")
    else:
        st.warning(f"📉 Sygnał: KUPUJ ZŁOTO (GSR < {gsr_limit})")

with col2:
    st.subheader("Strategia Ryzyka (BTC / Gold)")
    st.metric("Aktualne BTC/Gold", f"{curr_btc_gold:.2f}")
    if curr_btc_gold >= btc_gold_high:
        st.warning(f"🟡 Sygnał: ROTACJA DO ZŁOTA (BTC/Gold >= {btc_gold_high})")
    elif curr_btc_gold <= btc_gold_low:
        st.success(f"₿ Sygnał: KUPUJ BITCOINA (BTC/Gold <= {btc_gold_low})")
    else:
        st.info("⚖️ Status: Neutralny (wewnątrz przedziału)")

# --- WYKRESY ---
st.markdown("---")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['GSR'], name='GSR'))
fig.add_hline(y=gsr_limit, line_color="red", line_dash="dash")
st.plotly_chart(fig, use_container_width=True)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=data.index, y=data['BTC_Gold'], name='BTC/Gold'))
fig2.add_hline(y=btc_gold_high, line_color="orange", line_dash="dash")
fig2.add_hline(y=btc_gold_low, line_color="green", line_dash="dash")
st.plotly_chart(fig2, use_container_width=True)
