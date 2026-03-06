import streamlit as st
import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()
API_KEY = os.getenv("HG_API_KEY")

st.set_page_config(page_title="B3Radar", page_icon="📡", layout="wide")
st.title("📡 B3Radar — Dashboard B3")
st.markdown("---")

# ─────────────────────────────────────────────
# BLUE CHIPS MONITORADAS
# ─────────────────────────────────────────────

BLUE_CHIPS = [
    "PETR4", "VALE3", "ITUB4", "BBDC4",
    "WEGE3", "MGLU3", "BBAS3", "ITSA4",
    "RENT3", "ABEV3", "ELET3", "SUZB3",
    "RDOR3", "EQTL3", "HAPV3"
]

# ─────────────────────────────────────────────
# FUNÇÕES DE DADOS
# ─────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_finance_data():
    """Busca IBOV, Dólar e ações via HG Brasil Finance API."""
    try:
        url = (
            f"https://api.hgbrasil.com/finance"
            f"?format=json"
            f"&key={API_KEY}"
            f"&fields=only_results"
        )
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return None


@st.cache_data(ttl=600)
def get_historico(simbolo):
    """Busca histórico de preços dos últimos 30 dias via HG Brasil."""
    try:
        url = (
            f"https://api.hgbrasil.com/finance/stock_price"
            f"?key={API_KEY}"
            f"&symbol={simbolo}"
            f"&date_start=30"
        )
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        dados = resp.json()
        resultados = dados["results"][simbolo]["prices"]
        df = pd.DataFrame(resultados)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").set_index("date")
        return df[["price"]]
    except Exception:
        return None


def extrair_acao(data, simbolo):
    """Extrai preço e variação de uma ação do retorno da API."""
    try:
        acao = data["results"]["stocks"][simbolo]
        return {
            "preco": acao.get("price", 0.0),
            "variacao": acao.get("change_percent", 0.0),
        }
    except Exception:
        return {"preco": 0.0, "variacao": 0.0}


def extrair_ibov(data):
    """Extrai dados do Ibovespa."""
    try:
        ibov = data["results"]["indexes"]["IBOVESPA"]
        return {
            "preco": ibov["points"],
            "variacao": ibov["change_percent"],
        }
    except Exception:
        return {"preco": 0.0, "variacao": 0.0}


def extrair_dolar(data):
    """Extrai dados do Dólar (USD)."""
    try:
        dolar = data["results"]["currencies"]["USD"]
        return {
            "preco": dolar["buy"],
            "variacao": dolar["variation"],
        }
    except Exception:
        return {"preco": 0.0, "variacao": 0.0}


# ─────────────────────────────────────────────
# BUSCA DOS DADOS
# ─────────────────────────────────────────────

data = get_finance_data()

if data is None:
    st.warning("⚠️ Não foi possível carregar os dados. Verifique sua API Key no arquivo .env")
    st.stop()

ibov  = extrair_ibov(data)
dolar = extrair_dolar(data)
acoes_data = {simbolo: extrair_acao(data, simbolo) for simbolo in BLUE_CHIPS}

# ─────────────────────────────────────────────
# MÉTRICAS PRINCIPAIS
# ─────────────────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "📈 IBOVESPA",
        f"{ibov['preco']:,.0f} pts",
        f"{ibov['variacao']:+.2f}%"
    )
with col2:
    st.metric(
        "💵 DÓLAR",
        f"R$ {dolar['preco']:.2f}",
        f"{dolar['variacao']:+.2f}%"
    )

st.markdown("---")

# ─────────────────────────────────────────────
# TABELA DE BLUE CHIPS
# ─────────────────────────────────────────────

st.subheader("📊 Blue Chips Monitoradas")

acoes_lista = [
    {
        "Ticker": simbolo,
        "Preço (R$)": acoes_data[simbolo]["preco"],
        "Variação (%)": acoes_data[simbolo]["variacao"],
    }
    for simbolo in BLUE_CHIPS
]

acoes_df = pd.DataFrame(acoes_lista)

top_altas  = acoes_df.nlargest(3, "Variação (%)")
top_baixas = acoes_df.nsmallest(3, "Variação (%)")

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.markdown("#### 🔥 Top 3 Altas")
    st.dataframe(
        top_altas,
        column_config={
            "Preço (R$)":   st.column_config.NumberColumn(format="R$ %.2f"),
            "Variação (%)": st.column_config.NumberColumn(format="%.2f%%"),
        },
        use_container_width=True,
        hide_index=True,
    )

with col_t2:
    st.markdown("#### 📉 Top 3 Baixas")
    st.dataframe(
        top_baixas,
        column_config={
            "Preço (R$)":   st.column_config.NumberColumn(format="R$ %.2f"),
            "Variação (%)": st.column_config.NumberColumn(format="%.2f%%"),
        },
        use_container_width=True,
        hide_index=True,
    )

st.markdown("#### 📋 Todas as Ações")
st.dataframe(
    acoes_df,
    column_config={
        "Preço (R$)":   st.column_config.NumberColumn(format="R$ %.2f"),
        "Variação (%)": st.column_config.NumberColumn(format="%.2f%%"),
    },
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ─────────────────────────────────────────────
# GRÁFICO DE HISTÓRICO
# ─────────────────────────────────────────────

st.subheader("📈 Histórico de Preço — Últimos 30 dias")

acao_selecionada = st.selectbox(
    "Selecione uma ação:",
    options=BLUE_CHIPS,
    index=0
)

with st.spinner(f"Carregando histórico de {acao_selecionada}..."):
    historico = get_historico(acao_selecionada)

if historico is not None and not historico.empty:
    st.line_chart(historico, use_container_width=True)
else:
    st.info("ℹ️ Histórico não disponível para essa ação no momento.")

st.markdown("---")

# ─────────────────────────────────────────────
# ALERTAS DE PREÇO
# ─────────────────────────────────────────────

st.subheader("🔔 Alertas de Preço")

col_a1, col_a2 = st.columns(2)

with col_a1:
    ticker_alerta = st.selectbox("Ação", options=BLUE_CHIPS, key="alerta_ticker")
    alvo = st.number_input("Alertar acima de R$", value=0.0, step=0.5)
    preco_atual = acoes_data[ticker_alerta]["preco"]
    if alvo > 0:
        if preco_atual > alvo:
            st.error(f"🚨 {ticker_alerta} em R$ {preco_atual:.2f} — ACIMA DO ALVO!")
        else:
            st.success(f"✅ {ticker_alerta} em R$ {preco_atual:.2f} — abaixo do alvo.")

st.markdown("---")

# ─────────────────────────────────────────────
# EXPORTAR
# ─────────────────────────────────────────────

st.subheader("📥 Exportar Dados")

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.download_button(
        label="📈 Baixar CSV",
        data=acoes_df.to_csv(index=False),
        file_name="b3radar.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col_e2:
    resumo = (
        f"B3Radar — {time.strftime('%d/%m/%Y %H:%M')}\n"
        f"IBOV:  {ibov['preco']:,.0f} pts ({ibov['variacao']:+.2f}%)\n"
        f"Dólar: R$ {dolar['preco']:.2f} ({dolar['variacao']:+.2f}%)\n\n"
        + "\n".join(
            f"{s}: R$ {acoes_data[s]['preco']:.2f} ({acoes_data[s]['variacao']:+.2f}%)"
            for s in BLUE_CHIPS
        )
    )
    st.download_button(
        label="📋 Baixar Resumo .txt",
        data=resumo,
        file_name="b3radar_resumo.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.markdown("---")

# ─────────────────────────────────────────────
# ATUALIZAR
# ─────────────────────────────────────────────

if st.button("🔄 Atualizar Dados", type="primary", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.caption(f"Última atualização: {time.strftime('%d/%m/%Y %H:%M:%S')} · Dados: HG Brasil Finance API")