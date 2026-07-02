import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Konfiguracja strony Streamlit
st.set_page_config(
    page_title="Hard Assets Ratio Advisor — Chmura",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Nagłówek aplikacji
st.title("🪙 Hard Assets Ratio Advisor")
st.subheader("Automatyczny doradca i dashboard inwestycyjny dla złota, srebra i Bitcoina")

# --- SIDEBAR: USTAWIENIA PROGÓW I DANYCH ---
st.sidebar.header("⚙️ Ustawienia Progów i Danych")

# Wybór zakresu danych
range_option = st.sidebar.selectbox(
    "Zakres danych historycznych:",
    options=["1y", "3y", "5y", "10y", "max"],
    index=2
)

st.sidebar.markdown("---")

# Progi dla Gold-Silver Ratio
st.sidebar.subheader("📊 Progi dla Gold-Silver Ratio (GSR)")
gsr_low = st.sidebar.slider("Niski próg GSR (Kupuj Złoto):", min_value=40, max_value=100, value=65)
gsr_high = st.sidebar.slider("Wysoki próg GSR (Kupuj Srebro):", min_value=40, max_value=100, value=80)

st.sidebar.markdown("---")

# Progi dla BTC / Gold Ratio
st.sidebar.subheader("₿ Progi dla BTC / Gold Ratio")
btc_gold_low = st.sidebar.slider("Niski próg BTC/Gold (Kupuj BTC):", min_value=5, max_value=50, value=15)
btc_gold_high = st.sidebar.slider("Wysoki próg BTC/Gold (Kupuj Złoto):", min_value=5, max_value=50, value=25)

# --- POBIERANIE DANYCH Z YAHOO FINANCE ---
@st.cache_data(ttl=3600)  # Dane będą zapisane w pamięci podręcznej przez 1 godzinę
def load_data(period):
    # Tickery: GC=F (Złoto), SI=F (Srebro), BTC-USD (Bitcoin)
    tickers = {
        'Gold': 'GC=F',
        'Silver': 'SI=F',
        'BTC': 'BTC-USD'
    }
    
    df_final = pd.DataFrame()
    
    for name, ticker in tickers.items():
        data = yf.download(ticker, period=period)
        if not data.empty:
            # Wyciągamy cenę zamknięcia ('Close') jako serię jednowymiarową
            close_series = data['Close'].squeeze()
            df_final[name] = close_series
            
    # Czyszczenie danych (usuwanie dni wolnych, gdzie np. krypto działa, a giełda metali nie)
    df_final = df_final.ffill().dropna()
    return df_final

with st.spinner("🔄 Pobieranie najświeższych danych rynkowych z Yahoo Finance..."):
    try:
        data = load_data(range_option)
        
        if data.empty or len(data) < 2:
            st.error("Brak wystarczającej ilości danych rynkowych dla wybranego okresu.")
        else:
            # Obliczanie wskaźników (Ratios)
            data['GSR'] = data['Gold'] / data['Silver']
            data['BTC_Gold'] = data['BTC'] / data['Gold']
            
            # Pobranie ostatnich aktualnych wartości
            current_gold = data['Gold'].iloc[-1]
            current_silver = data['Silver'].iloc[-1]
            current_btc = data['BTC'].iloc[-1]
            current_gsr = data['GSR'].iloc[-1]
            current_btc_gold = data['BTC_Gold'].iloc[-1]
            
            # --- WIDGETY Z AKTUALNYMI CENAMI ---
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Złoto (USD/oz)", f"${current_gold:,.2f}")
            col2.metric("Srebro (USD/oz)", f"${current_silver:,.2f}")
            col3.metric("Bitcoin (USD)", f"${current_btc:,.2f}")
            col4.metric("Gold-Silver Ratio", f"{current_gsr:.2f}")
            col5.metric("BTC / Gold Ratio", f"{current_btc_gold:.2f}")
            
            st.markdown("---")
            
            # --- GENEROWANIE SYGNAŁÓW ADVISORA ---
            st.subheader("💡 Aktualne Sugestie Strategiczne")
            sig_col1, sig_col2 = st.columns(2)
            
            with sig_col1:
                st.markdown("### **Strategia Metali (GSR)**")
                if current_gsr >= gsr_high:
                    st.success(f"📈 **Sygnał: KUPUJ SREBRO.** Wskaźnik GSR ({current_gsr:.2f}) jest powyżej progu {gsr_high}. Srebro jest historycznie tanie względem złota.")
                elif current_gsr <= gsr_low:
                    st.warning(f"📉 **Sygnał: KUPUJ ZŁOTO.** Wskaźnik GSR ({current_gsr:.2f}) jest poniżej progu {gsr_low}. Złoto jest historycznie tanie względem srebra.")
                else:
                    st.info(f"⚖️ **Status: NEUTRALNY.** Wskaźnik GSR ({current_gsr:.2f}) znajduje się wewnątrz strefy równowagi.")
                    
            with sig_col2:
                st.markdown("### **Strategia Ryzyka (BTC / Gold)**")
                if current_btc_gold >= btc_gold_high:
                    st.warning(f"🟡 **Sygnał: ROTACJA DO ZŁOTA.** Wskaźnik ({current_btc_gold:.2f}) przekroczył próg {btc_gold_high}. Bitcoin może być lokalnie przewartościowany względem złota.")
                elif current_btc_gold <= btc_gold_low:
                    st.success(f"₿ **Sygnał: ROTACJA DO BITCOINA.** Wskaźnik ({current_btc_gold:.2f}) spadł poniżej progu {btc_gold_low}. Bitcoin jest atrakcyjny cenowo względem złota.")
                else:
                    st.info(f"⚖️ **Status: NEUTRALNY.** Relacja BTC do Złota ({current_btc_gold:.2f}) w normie rynkowej.")

            st.markdown("---")
            
            # --- WYKRESY INTERAKTYWNE ---
            st.subheader("📈 Wykresy Historyczne Wskaźników")
            
            # Wykres 1: Gold-Silver Ratio
            fig_gsr = go.Figure()
            fig_gsr.add_trace(go.Scatter(x=data.index, y=data['GSR'], mode='lines', name='GSR', line=dict(color='#FFD700', width=2)))
            fig_gsr.add_hline(y=gsr_high, line_dash="dash", line_color="red", annotation_text="Kupuj Srebro (Wysoki próg)")
            fig_gsr.add_hline(y=gsr_low, line_dash="dash", line_color="green", annotation_text="Kupuj Złoto (Niski próg)")
            fig_gsr.update_layout(title="Historia wskaźnika Gold-Silver Ratio (GSR)", template="plotly_dark", height=400)
            st.plotly_chart(fig_gsr, use_container_width=True)
            
            # Wykres 2: BTC / Gold Ratio
            fig_btc_gold = go.Figure()
            fig_btc_gold.add_trace(go.Scatter(x=data.index, y=data['BTC_Gold'], mode='lines', name='BTC/Gold', line=dict(color='#00F0FF', width=2)))
            fig_btc_gold.add_hline(y=btc_gold_high, line_dash="dash", line_color="orange", annotation_text="Rotacja do Złota (Drogi BTC)")
            fig_btc_gold.add_hline(y=btc_gold_low, line_dash="dash", line_color="lightgreen", annotation_text="Rotacja do BTC (Tani BTC)")
            fig_btc_gold.update_layout(title="Historia wskaźnika Bitcoin / Gold Ratio", template="plotly_dark", height=400)
            st.plotly_chart(fig_btc_gold, use_container_width=True)

    except Exception as e:
        st.error(f"Wystąpił błąd podczas ładowania lub przetwarzania danych: {e}")
        st.info("Upewnij się, że masz połączenie z internetem. Yahoo Finance może chwilowo nie odpowiadać.")
