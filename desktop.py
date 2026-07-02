import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="NEO ASSET ADVISOR", layout="wide")

# --- CSS: CZYTELNY TERMINAL ---
st.markdown("""
    <style>
    .big-font { font-size: 50px !important; font-weight: bold; text-align: center; color: #00FF41; }
    .status-box { padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #00FF41; background: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("// SYSTEM: HARD ASSET ADVISOR")

# --- DANE ---
@st.cache_data(ttl=3600)
def load_data():
    tickers = {'Gold': 'GC=F', 'Silver': 'SI=F', 'BTC': 'BTC-USD'}
    df = pd.DataFrame()
    for n, t in tickers.items():
        df[n] = yf.download(t, period="2y")['Close'].squeeze()
    return df.ffill().dropna()

data = load_data()
gsr = data['Gold'].iloc[-1] / data['Silver'].iloc[-1]
btc_gold = data['BTC'].iloc[-1] / data['Gold'].iloc[-1]

# --- SEKCJA GŁÓWNA: SZYBKA DECYZJA ---
st.markdown("---")
st.subheader("🚀 NATYCHMIASTOWA REKOMENDACJA")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 📊 METALE (GSR)")
    if gsr >= 80:
        st.markdown("<div class='status-box' style='color:#00FF41;'>KUPUJ SREBRO<br>GSR jest wysoki (Tanio vs Złoto)</div>", unsafe_allow_html=True)
    elif gsr <= 60:
        st.markdown("<div class='status-box' style='color:#FFD700;'>KUPUJ ZŁOTO<br>GSR jest niski (Tanio vs Srebro)</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-box' style='color:#aaaaaa;'>STATUS NEUTRALNY<br>Czekaj na okazję</div>", unsafe_allow_html=True)

with col_b:
    st.markdown("### ₿ RYNEK (BTC/GOLD)")
    if btc_gold >= 40:
        st.markdown("<div class='status-box' style='color:#FFD700;'>ROTACJA DO ZŁOTA<br>BTC bardzo drogie względem Złota</div>", unsafe_allow_html=True)
    elif btc_gold <= 15:
        st.markdown("<div class='status-box' style='color:#00FF41;'>KUPUJ BITCOINA<br>BTC bardzo tanie względem Złota</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-box' style='color:#aaaaaa;'>STATUS NEUTRALNY<br>Czekaj na okazję</div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📉 TRENDY HISTORYCZNE (Dla weryfikacji)")
# Tu zostają Twoje wykresy z poprzedniego kroku (możesz wkleić ten sam kod wykresów co poprzednio)
