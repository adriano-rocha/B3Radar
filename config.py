TELEGRAM_TOKEN   = "SEU_TOKEN"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID"

# Carteira Ibovespa — tickers validados no yfinance (abr/2026)
# Tickers corrigidos:
#   ELET3/ELET6 → AXIA3/AXIA6  (Eletrobras rebrandeou para Axia Energia em nov/2025)
#   RUMO3       → RAIL3         (mudança antiga, yfinance só reconhece RAIL3)
#   CCRO3       → MOVI3         (CCR rebrandeou para Motiva)
#   SOMA3       → removido      (fundiu com Arezzo, virou AZZA3 — já está na lista)
#   ALLOS3      → ALSO3         (yfinance não reconhece ALLOS3)
#   MRFG3       → removido      (fusão com BRF, usar BEEF3 que já está na lista)
#   CPLE6       → CPLE3         (yfinance não encontra CPLE6)
#   TRPL4       → ISAE4         (ISA Energia rebrandeou)

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
    "WEGE3", "EMBR3", "TOTS3", "POMO4",
    # Imóveis & Shopping
    "MULT3", "ALSO3", "IGTI11",
    # Saneamento
    "SBSP3",
    # Petroquímica
    "BRKM5",
    # Diversificado
    "UGPA3", "RAIZ4", "CSAN3", "BEEF3",
    "NTCO3", "SMFT3", "TAEE11", "ISAE4", "RANI3",
    # B3 e outros
    "B3SA3", "JBSS3",
]

# Timeframe principal (contexto)
INTERVALO = "15m"
PERIODO   = "5d"

# MÉDIAS
MM_RAPIDA    = 9
MM_LENTA     = 21
MM_TENDENCIA = 21

# SUPORTE / RESISTÊNCIA
JANELA_SR = 20

# VOLUME
VOLUME_FATOR  = 1.8
VOLUME_JANELA = 20

# HORÁRIO
HORA_INICIO = "10:05"
HORA_FIM    = "16:30"

# CONTROLE DE QUALIDADE
DISTANCIA_MAX = 0.01
SCORE_MINIMO  = 2