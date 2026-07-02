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
    .stApp { background-color: #0d0208; color: #00FF41; font-family: 'Orbitron', sans-serif; }
    .action-box { 
        padding: 20px; 
        border: 2px solid #00FF41; 
        border-radius: 10px; 
        background: #001a00; 
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
    }
    .status-text { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    h1, h2, h3 { color: #00FF41 !important; text-transform: uppercase; text-shadow: 0 0 10px #00FF41; }
    </style>
""", unsafe_allow_html=True)

st.title("// SYSTEM: HARD ASSETS ADVISOR")

# --- LOGIKA ---
@st.cache_data(ttl=3600)
def load_data():
    df = pd.DataFrame()
    for n, t in {'Gold': 'GC=F', 'Silver': 'SI=F', 'BTC': 'BTC-USD'}.items():
        df[n] = yf.download(t, period="5y")['Close'].squeeze()
    return df.ffill().dropna()

data = load_data()
gsr = data['Gold'].iloc[-1] / data['Silver'].iloc[-1]
btc_gold = data['BTC'].iloc[-1] / data['Gold'].iloc[-1]

# --- DASHBOARD DECYZYJNY ---
st.subheader("💡 SYSTEM RECOMMENDATIONS")
c1, c2 = st.columns(2)

# Logika GSR
with c1:
    st.markdown("### METALS STRATEGY (GSR)")
    box_content = ""
    if gsr >= 80:
        box_content = "<div class='action-box' style='border-color: #FF0055;'><div class='status-text'>KUPUJ SREBRO</div>Srebro jest ekstremalnie tanie w stosunku do złota. Akumuluj Srebro.</div>"
    elif gsr <= 60:
        box_content = "<div class='action-box' style='border-color: #FFD700;'><div class='status-text'>KUPUJ ZŁOTO</div>Srebro jest drogie względem złota. Przejdź na bezpieczne Złoto.</div>"
    else:
        box_content = "<div class='action-box' style='border-color: #00FF41;'><div class='status-text'>STATUS NEUTRALNY</div>GSR w normie. Trzymaj obecne pozycje.</div>"
    st.markdown(box_content, unsafe_allow_html=True)

# Logika BTC/GOLD
with c2:
    st.markdown("### BTC/GOLD STRATEGY")
    box_content = ""
    if btc_gold >= 40:
        box_content = "<div class='action-box' style='border-color: #FFD700;'><div class='status-text'>ROTACJA DO ZŁOTA</div>BTC jest przewartościowane. Wymień BTC na Złoto.</div>"
    elif btc_gold <= 15:
        box_content = "<div class='action-box' style='border-color: #00FF41;'><div class='status-text'>KUPUJ BITCOINA</div>BTC jest bardzo tanie względem Złota. Accumuluj BTC.</div>"
    else:
        box_content = "<div class='action-box' style='border-color: #00FF41;'><div class='status-text'>STATUS NEUTRALNY</div>Relacja w normie. Czekaj na sygnał.</div>"
    st.markdown(box_content, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📈 CORE ANALYTICS VISUALIZATION")

# --- WYKRESY ---
def draw_chart(df, col, title, high_val, low_val, color_high, color_low):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, line=dict(color='#00FF41')))
    fig.add_hline(y=high_val, line_dash="dash", line_color=color_high, annotation_text="Limit Górny")
    fig.add_hline(y=low_val, line_dash="dash", line_color=color_low, annotation_text="Limit Dolny")
    fig.update_layout(template="plotly_dark", title=title, plot_bgcolor='#0d0208', paper_bgcolor='#0d0208')
    st.plotly_chart(fig, use_container_width=True)

draw_chart(data, 'GSR', "GSR: ZŁOTO vs SREBRO", 80, 60, "#FF0055", "#00F0FF")
draw_chart(data, 'BTC_Gold', "BTC/GOLD: RYZYKO vs BEZPIECZEŃSTWO", 40, 15, "#FF9900", "#00FF66")
