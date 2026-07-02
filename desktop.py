import subprocess
import time
import webview
import sys

def start_desktop_app():
    # 1. Uruchamiamy Streamlit "po cichu" w tle (headless)
    # Używamy sys.executable, aby upewnić się, że odpala się z tego samego środowiska
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "true", "--server.port", "8501"]
    )
    
    # 2. Dajemy serwerowi 3 sekundy na wystartowanie
    time.sleep(3)
    
    # 3. Otwieramy natywne, czyste okno systemowe skierowane na naszą aplikację
    window = webview.create_window(
        title="Hard Assets Ratio Advisor — Desktop", 
        url="http://localhost:8501",
        width=1280,
        height=800,
        resizable=True
    )
    
    # 4. Uruchamiamy okno (gdy użytkownik je zamknie, kod przejdzie dalej)
    webview.start()
    
    # 5. Po zamknięciu okna automatycznie i bezpiecznie wyłączamy proces Streamlita w tle
    streamlit_process.terminate()

if __name__ == "__main__":
    start_desktop_app()