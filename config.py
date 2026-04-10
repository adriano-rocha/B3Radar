TELEGRAM_TOKEN   = "SEU_TOKEN"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID"

TICKERS = [
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
    # "EMBR3",   # ⚠️ Indisponível no Yahoo Finance (abr/2026)
    # Imóveis & Shopping
    "MULT3", "IGTI11",
    # "ALSO3",   # ⚠️ Ticker incorreto — ALLOS3 também falha no yfinance
    # Saneamento
    "SBSP3",
    # Petroquímica
    "BRKM5",
    # Diversificado
    "UGPA3", "RAIZ4", "CSAN3", "BEEF3",
    # "NTCO3",   # ⚠️ Indisponível — Natura&Co em reestruturação
    "SMFT3", "TAEE11", "ISAE4", "RANI3",
    # B3 e outros
    "B3SA3",
    # "JBSS3",   # ⚠️ Temporariamente indisponível no Yahoo Finance
]

# ── Timeframe principal ────────────────────────────────────────────────────────
INTERVALO = "15m"
PERIODO   = "5d"

# ── Médias Móveis ──────────────────────────────────────────────────────────────
MM_RAPIDA    = 9
MM_LENTA     = 21
MM_TENDENCIA = 21

# ── Suporte / Resistência ──────────────────────────────────────────────────────
JANELA_SR = 20

# ── Volume ─────────────────────────────────────────────────────────────────────
VOLUME_FATOR  = 1.8
VOLUME_JANELA = 20

# ── Horário de operação ────────────────────────────────────────────────────────
HORA_INICIO = "10:05"
HORA_FIM    = "16:30"

# ── Controle de qualidade ──────────────────────────────────────────────────────
DISTANCIA_MAX = 0.01
SCORE_MINIMO  = 2