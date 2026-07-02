import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="NEO ASSET ADVISOR", layout="wide")

# --- STYLIZACJA CYBERPUNK / MATRIX ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background-color: #0d0208;
        color: #00FF41;
        font-family: 'Orbitron', sans-serif;
    }
    h1, h2, h3 {
        color: #008F11 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00FF41;
    }
    .stMetric {
        background-color: #001a00;
        border: 1px solid #00FF41;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("// SYSTEM: HARD ASSETS ADVISOR")
st.subheader("INITIALIZING MARKET DATA...")

# --- LOGIKA (bez zmian w wartościach) ---
gsr_low, gsr_high = 60, 80
btc_gold_low, btc_gold_high = 15, 40

@st.cache_data(ttl=3600)
def load_data():
    df = pd.DataFrame()
    for n, t in {'Gold': 'GC=F', 'Silver': 'SI=F', 'BTC': 'BTC-USD'}.items():
        df[n] = yf.download(t, period="5y")['Close'].squeeze()
    return df.ffill().dropna()

data = load_data()
data['GSR'] = data['Gold'] / data['Silver']
data['BTC_Gold'] = data['BTC'] / data['Gold']

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("GOLD (OZ)", f"${data['Gold'].iloc[-1]:,.2f}")
col2.metric("SILVER (OZ)", f"${data['Silver'].iloc[-1]:,.2f}")
col3.metric("BTC (USD)", f"${data['BTC'].iloc[-1]:,.2f}")
col4.metric("GSR", f"{data['GSR'].iloc[-1]:.2f}")
col5.metric("BTC/GOLD", f"{data['BTC_Gold'].iloc[-1]:.2f}")

# --- WYKRESY Z MOTYWEM MATRIX ---
def make_matrix_chart(df, col_name, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[col_name], line=dict(color='#00FF41', width=2)))
    fig.update_layout(
        title=title,
        plot_bgcolor='#0d0208',
        paper_bgcolor='#0d0208',
        font=dict(color='#00FF41'),
        xaxis=dict(gridcolor='#003b00'),
        yaxis=dict(gridcolor='#003b00')
    )
    return fig

st.plotly_chart(make_matrix_chart(data, 'GSR', "GSR HISTORY // MATRIX ANALYSIS"), use_container_width=True)
st.plotly_chart(make_matrix_chart(data, 'BTC_Gold', "BTC/GOLD RATIO // CYBERNETIC TREND"), use_container_width=True)
