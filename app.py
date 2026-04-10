import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="B3Radar", page_icon="📡", layout="wide")
st.title("📡 B3Radar — Dashboard B3")
st.markdown("---")

# Carteira Ibovespa — tickers validados (abr/2026)
BLUE_CHIPS = [
    # Petróleo & Energia
    "PETR3", "PETR4", "PRIO3", "RECV3", "BRAV3", "VBBR3",
    # Mineração & Siderurgia
    "VALE3", "CSNA3", "CMIN3", "GGBR4", "GOAU4", "USIM5",
    # Bancos & Financeiro
    "ITUB4", "BBDC3", "BBDC4", "BBAS3", "SANB11", "BPAC11",
    "ITSA4", "BBSE3", "CXSE3", "IRBR3", "PSSA3",
    # Energia Elétrica
    "AXIA3", "AXIA6", "EQTL3", "EGIE3", "CMIG4", "CPFE3",
    "CPLE3", "ENEV3", "AURE3",
    # Telecomunicações
    "VIVT3", "TIMS3",
    # Consumo & Varejo
    "ABEV3", "LREN3", "MGLU3", "AZZA3", "CEAB3",
    "PCAR3", "ASAI3", "VIVA3",
    # Construção Civil
    "MRVE3", "CYRE3", "DIRR3", "CURY3",
    # Saúde
    "HAPV3", "RDOR3", "FLRY3", "RADL3", "HYPE3",
    # Educação
    "YDUQ3", "COGN3",
    # Papel & Celulose
    "SUZB3", "KLBN11",
    # Logística & Infraestrutura
    "RAIL3", "MOVI3",
    # Agronegócio
    "SLCE3",
    # Indústria & Outros
    "WEGE3", "TOTS3", "POMO4",
    # Imóveis & Shopping
    "MULT3", "IGTI11",
    # Saneamento
    "SBSP3",
    # Petroquímica
    "BRKM5",
    # Diversificado
    "UGPA3", "RAIZ4", "CSAN3", "BEEF3",
    "SMFT3", "TAEE11", "ISAE4", "RANI3",
    # B3 e outros
    "B3SA3",
]

# ── FUNÇÕES DE DADOS ──────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_ibov():
    try:
        ticker = yf.Ticker("^BVSP")
        hist = ticker.history(period="2d")
        if hist.empty:
            return {"preco": 0.0, "variacao": 0.0}
        preco_atual    = hist["Close"].iloc[-1]
        preco_anterior = hist["Close"].iloc[-2] if len(hist) > 1 else preco_atual
        variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
        return {"preco": float(preco_atual), "variacao": float(variacao)}
    except Exception:
        return {"preco": 0.0, "variacao": 0.0}


@st.cache_data(ttl=300)
def get_dolar():
    try:
        ticker = yf.Ticker("USDBRL=X")
        hist = ticker.history(period="2d")
        if hist.empty:
            return {"preco": 0.0, "variacao": 0.0}
        preco_atual    = hist["Close"].iloc[-1]
        preco_anterior = hist["Close"].iloc[-2] if len(hist) > 1 else preco_atual
        variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
        return {"preco": float(preco_atual), "variacao": float(variacao)}
    except Exception:
        return {"preco": 0.0, "variacao": 0.0}


@st.cache_data(ttl=300)
def get_acoes(simbolos):
    tickers = [s + ".SA" for s in simbolos]
    resultado = {}
    try:
        dados = yf.download(tickers, period="2d", progress=False, auto_adjust=True)
        close = dados["Close"]
        for simbolo, ticker in zip(simbolos, tickers):
            try:
                serie = close[ticker].dropna()
                if len(serie) >= 2:
                    preco    = serie.iloc[-1]
                    anterior = serie.iloc[-2]
                    variacao = ((preco - anterior) / anterior) * 100
                elif len(serie) == 1:
                    preco    = serie.iloc[-1]
                    variacao = 0.0
                else:
                    preco, variacao = 0.0, 0.0
                resultado[simbolo] = {"preco": float(preco), "variacao": float(variacao)}
            except Exception:
                resultado[simbolo] = {"preco": 0.0, "variacao": 0.0}
    except Exception:
        for simbolo in simbolos:
            resultado[simbolo] = {"preco": 0.0, "variacao": 0.0}
    return resultado


@st.cache_data(ttl=600)
def get_historico(simbolo):
    try:
        ticker = yf.Ticker(simbolo + ".SA")
        hist   = ticker.history(period="30d")
        if hist.empty:
            return None
        return hist[["Close"]].rename(columns={"Close": "price"})
    except Exception:
        return None


# ── BUSCA DOS DADOS ───────────────────────────────────────────────────────────

ibov       = get_ibov()
dolar      = get_dolar()
acoes_data = get_acoes(BLUE_CHIPS)

# ── MÉTRICAS PRINCIPAIS ───────────────────────────────────────────────────────

col1, col2 = st.columns(2)
with col1:
    st.metric("📈 IBOVESPA", f"{ibov['preco']:,.0f} pts", f"{ibov['variacao']:+.2f}%")
with col2:
    st.metric("💵 DÓLAR", f"R$ {dolar['preco']:.2f}", f"{dolar['variacao']:+.2f}%")

st.markdown("---")

# ── TABELA DE AÇÕES ───────────────────────────────────────────────────────────

st.subheader("📊 Ações do Ibovespa Monitoradas")

acoes_lista = [
    {
        "Ticker":       simbolo,
        "Preço (R$)":   acoes_data[simbolo]["preco"],
        "Variação (%)": acoes_data[simbolo]["variacao"],
    }
    for simbolo in BLUE_CHIPS
]
acoes_df = pd.DataFrame(acoes_lista)

top_altas  = acoes_df.nlargest(3,  "Variação (%)")
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
        use_container_width=True, hide_index=True,
    )
with col_t2:
    st.markdown("#### 📉 Top 3 Baixas")
    st.dataframe(
        top_baixas,
        column_config={
            "Preço (R$)":   st.column_config.NumberColumn(format="R$ %.2f"),
            "Variação (%)": st.column_config.NumberColumn(format="%.2f%%"),
        },
        use_container_width=True, hide_index=True,
    )

st.markdown("#### 📋 Todas as Ações")
st.dataframe(
    acoes_df,
    column_config={
        "Preço (R$)":   st.column_config.NumberColumn(format="R$ %.2f"),
        "Variação (%)": st.column_config.NumberColumn(format="%.2f%%"),
    },
    use_container_width=True, hide_index=True,
)

st.markdown("---")

# ── GRÁFICO DE HISTÓRICO ──────────────────────────────────────────────────────

st.subheader("📈 Histórico de Preço — Últimos 30 dias")

acao_selecionada = st.selectbox("Selecione uma ação:", options=BLUE_CHIPS, index=0)

with st.spinner(f"Carregando histórico de {acao_selecionada}..."):
    historico = get_historico(acao_selecionada)

if historico is not None and not historico.empty:
    st.line_chart(historico, use_container_width=True)
else:
    st.info("ℹ️ Histórico não disponível para essa ação no momento.")

st.markdown("---")

# ── ALERTAS DE PREÇO ──────────────────────────────────────────────────────────

st.subheader("🔔 Alertas de Preço")

col_a1, _ = st.columns(2)
with col_a1:
    ticker_alerta = st.selectbox("Ação", options=BLUE_CHIPS, key="alerta_ticker")
    alvo          = st.number_input("Alertar acima de R$", value=0.0, step=0.5)
    preco_atual   = acoes_data[ticker_alerta]["preco"]
    if alvo > 0:
        if preco_atual > alvo:
            st.error(f"🚨 {ticker_alerta} em R$ {preco_atual:.2f} — ACIMA DO ALVO!")
        else:
            st.success(f"✅ {ticker_alerta} em R$ {preco_atual:.2f} — abaixo do alvo.")

st.markdown("---")

# ── EXPORTAR DADOS ────────────────────────────────────────────────────────────

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

# ── REFRESH ───────────────────────────────────────────────────────────────────

if st.button("🔄 Atualizar Dados", type="primary", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.caption(f"Última atualização: {time.strftime('%d/%m/%Y %H:%M:%S')} · Dados: Yahoo Finance")