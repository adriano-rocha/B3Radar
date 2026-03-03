import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="B3Radar",
    page_icon="📡",
    layout="wide"
)

st.title("📡 B3Radar - Mercado em Tempo Real")
st.markdown("---")

@st.cache_data(ttl=120)  # Cache 2 minutos
def get_bovespa_robust():
    """Versão robusta que trata erros do yfinance"""
    try:
        ticker = yf.Ticker("^BVSP")
        data = ticker.history(period="5d")  # 5 dias p/ garantir dados
        if not data.empty and "Close" in data.columns:
            return data["Close"].iloc[-1]
        else:
            return None
    except Exception:
        return None

# EXECUÇÃO
if __name__ == "__main__":
    with st.spinner("🔄 Carregando Ibovespa..."):
        valor = get_bovespa_robust()
    
    col1, col2 = st.columns(2)
    with col1:
        if valor:
            st.metric("Ibovespa Atual", f"{valor:,.0f}")
            st.success("✅ Dados carregados!")
        else:
            st.metric("Ibovespa Atual", "📈 Fora do horário", delta="Mercado fechado")
            st.info("💡 Mercado B3: Seg-Sex 10h-17h")    
    
    
    st.markdown("---")
    
