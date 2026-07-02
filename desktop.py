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
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Konfiguracja strony Streamlit
st.set_page_config(
    page_title="Hard Assets Ratio Advisor — SYSTEM",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLIZACJA CYBERPUNK / MATRIX (Niestandardowy CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* Główny kontener aplikacji */
    .stApp {
        background-color: #0d0208;
        color: #00FF41;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Nagłówki h1, h2, h3 z efektem neonu */
    h1, h2, h3 {
        color: #00FF41 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00FF41, 0 0 20px #008F11;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Sidebar (panel boczny) */
    [data-testid="stSidebar"] {
        background-color: #070104 !important;
        border-right: 1px solid #00FF41;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #00FF41 !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Metryki / Widgety z cenami */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #00FF41 !important;
        text-shadow: 0 0 5px #00FF41;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #008F11 !important;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] {
        background-color: #001a00 !important;
        border: 1px solid #00FF41 !important;
        padding: 15px !important;
        border-radius: 5px !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    
    /* Linie podziału */
    hr {
        border-color: #003b00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Nagłówek aplikacji
st.title("// SYSTEM: HARD ASSETS ADVISOR")
st.subheader("INITIALIZING MARKET CORE // GOLD, SILVER, BITCOIN")

# --- SIDEBAR: USTAWIENIA PROGÓW I DANYCH ---
st.sidebar.header("⚙️ SYSTEM CONFIG")

# Wybór zakresu danych
range_option = st.sidebar.selectbox(
    "TIMELINE RANGE:",
    options=["1y", "3y", "5y", "10y", "max"],
    index=2
)

st.sidebar.markdown("---")

# Progi dla Gold-Silver Ratio
st.sidebar.subheader("📊 GSR MATRIX LIMITS")
gsr_low = st.sidebar.slider("GSR LOW (BUY GOLD):", min_value=40, max_value=100, value=60)
gsr_high = st.sidebar.slider("GSR HIGH (BUY SILVER):", min_value=40, max_value=100, value=80)

st.sidebar.markdown("---")

# Progi dla BTC / Gold Ratio
st.sidebar.subheader("₿ BTC / GOLD LIMITS")
btc_gold_low = st.sidebar.slider("BTC/GOLD LOW (BUY BTC):", min_value=5, max_value=50, value=15)
btc_gold_high = st.sidebar.slider("BTC/GOLD HIGH (BUY GOLD):", min_value=5, max_value=50, value=40)

# --- POBIERANIE DANYCH Z YAHOO FINANCE ---
@st.cache_data(ttl=3600)
def load_data(period):
    tickers = {
        'Gold': 'GC=F',
        'Silver': 'SI=F',
        'BTC': 'BTC-USD'
    }
    df_final = pd.DataFrame()
    for name, ticker in tickers.items():
        data = yf.download(ticker, period=period)
        if not data.empty:
            close_series = data['Close'].squeeze()
            df_final[name] = close_series
    df_final = df_final.ffill().dropna()
    return df_final

with st.spinner("⚡ ACCESSING YAHOO FINANCE DATABASE..."):
    try:
        data = load_data(range_option)
        
        if data.empty or len(data) < 2:
            st.error("ERROR: INSUFFICIENT MARKET DATA.")
        else:
            # Obliczanie wskaźników
            data['GSR'] = data['Gold'] / data['Silver']
            data['BTC_Gold'] = data['BTC'] / data['Gold']
            
            # Ostatnie wartości
            current_gold = data['Gold'].iloc[-1]
            current_silver = data['Silver'].iloc[-1]
            current_btc = data['BTC'].iloc[-1]
            current_gsr = data['GSR'].iloc[-1]
            current_btc_gold = data['BTC_Gold'].iloc[-1]
            
            # --- WIDGETY Z AKTUALNYMI CENAMI ---
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("GOLD (USD/OZ)", f"${current_gold:,.2f}")
            col2.metric("SILVER (USD/OZ)", f"${current_silver:,.2f}")
            col3.metric("BITCOIN (USD)", f"${current_btc:,.2f}")
            col4.metric("GSR VALUE", f"{current_gsr:.2f}")
            col5.metric("BTC / GOLD", f"{current_btc_gold:.2f}")
            
            st.markdown("---")
            
            # --- GENEROWANIE SYGNAŁÓW ADVISORA ---
            st.subheader("💡 SYSTEM RECOMMENDATIONS")
            sig_col1, sig_col2 = st.columns(2)
            
            with sig_col1:
                st.markdown("### **METALS STRATEGY (GSR)**")
                if current_gsr >= gsr_high:
                    st.success(f"📈 [SIGNAL: BUY SILVER] // GSR ({current_gsr:.2f}) ABOVE CRITICAL LIMIT {gsr_high}. SILVER UNDERVALUED.")
                elif current_gsr <= gsr_low:
                    st.warning(f"📉 [SIGNAL: BUY GOLD] // GSR ({current_gsr:.2f}) BELOW CRITICAL LIMIT {gsr_low}. GOLD UNDERVALUED.")
                else:
                    st.info(f"⚖️ [STATUS: NEUTRAL] // GSR ({current_gsr:.2f}) IN EQUILIBRIUM ZONE ({gsr_low}-{gsr_high}).")
                    
            with sig_col2:
                st.markdown("### **RISK STRATEGY (BTC / GOLD)**")
                if current_btc_gold >= btc_gold_high:
                    st.warning(f"🟡 [SIGNAL: ROTATE TO GOLD] // RATIO ({current_btc_gold:.2f}) EXCEEDED LIMIT {btc_gold_high}. BTC OVERVALUED.")
                elif current_btc_gold <= btc_gold_low:
                    st.success(f"₿ [SIGNAL: ROTATE TO BTC] // RATIO ({current_btc_gold:.2f}) DROPPED BELOW LIMIT {btc_gold_low}. BTC UNDERVALUED.")
                else:
                    st.info(f"⚖️ [STATUS: NEUTRAL] // RATIO ({current_btc_gold:.2f}) IN STANDBY ZONE ({btc_gold_low}-{btc_gold_high}).")

            st.markdown("---")
            
            # --- WYKRESY INTERAKTYWNE (Z POWROTEM Z LINIAMI PROGÓW) ---
            st.subheader("📈 CORE ANALYTICS VISUALIZATION")
            
            # Wykres 1: Gold-Silver Ratio
            fig_gsr = go.Figure()
            fig_gsr.add_trace(go.Scatter(x=data.index, y=data['GSR'], mode='lines', name='GSR', line=dict(color='#00FF41', width=2)))
            # Neonowe linie progów wejścia
            fig_gsr.add_hline(y=gsr_high, line_dash="dash", line_color="#FF0055", annotation_text="Kupuj Srebro (Próg Wysoki)", annotation_font_color="#FF0055")
            fig_gsr.add_hline(y=gsr_low, line_dash="dash", line_color="#00F0FF", annotation_text="Kupuj Złoto (Próg Niski)", annotation_font_color="#00F0FF")
            
            fig_gsr.update_layout(
                title="GSR DATABASE STREAM // DATA CORRELATION", 
                template="plotly_dark", 
                height=400,
                plot_bgcolor='#0d0208',
                paper_bgcolor='#0d0208',
                font=dict(color='#00FF41', family='Orbitron'),
                xaxis=dict(gridcolor='#002200'),
                yaxis=dict(gridcolor='#002200')
            )
            st.plotly_chart(fig_gsr, use_container_width=True)
            
            # Wykres 2: BTC / Gold Ratio
            fig_btc_gold = go.Figure()
            fig_btc_gold.add_trace(go.Scatter(x=data.index, y=data['BTC_Gold'], mode='lines', name='BTC/Gold', line=dict(color='#00FF41', width=2)))
            # Neonowe linie progów wejścia
            fig_btc_gold.add_hline(y=btc_gold_high, line_dash="dash", line_color="#FF9900", annotation_text="Rotacja do Złota (Drogi BTC)", annotation_font_color="#FF9900")
            fig_btc_gold.add_hline(y=btc_gold_low, line_dash="dash", line_color="#00FF66", annotation_text="Rotacja do BTC (Tani BTC)", annotation_font_color="#00FF66")
            
            fig_btc_gold.update_layout(
                title="BTC / GOLD RATIO STREAM // ALGORITHMIC TREND", 
                template="plotly_dark", 
                height=400,
                plot_bgcolor='#0d0208',
                paper_bgcolor='#0d0208',
                font=dict(color='#00FF41', family='Orbitron'),
                xaxis=dict(gridcolor='#002200'),
                yaxis=dict(gridcolor='#002200')
            )
            st.plotly_chart(fig_btc_gold, use_container_width=True)

    except Exception as e:
        st.error(f"SYSTEM CRITICAL ERROR: {e}")
        st.info("CONNECTION TIMEOUT // CHECK NETWORK GRID INTENSITY.")
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
