TELEGRAM_TOKEN   = "SEU_TOKEN"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID"

# Carteira Ibovespa — 85 ativos (carteira vigente jan/2026)
TICKERS = [
    # Petróleo & Energia
    "PETR3", "PETR4", "PRIO3", "RECV3", "BRAV3", "VBBR3",
    # Mineração & Siderurgia
    "VALE3", "CSNA3", "CMIN3", "GGBR4", "GOAU4", "USIM5",
    # Bancos & Financeiro
    "ITUB4", "BBDC3", "BBDC4", "BBAS3", "SANB11", "BPAC11",
    "ITSA4", "BBSE3", "CXSE3", "IRBR3", "PSSA3",
    # Energia Elétrica
    "ELET3", "ELET6", "EQTL3", "EGIE3", "CMIG4", "CPFE3",
    "CPLE6", "ENEV3", "AURE3",
    # Telecomunicações
    "VIVT3", "TIMS3",
    # Consumo & Varejo
    "ABEV3", "LREN3", "MGLU3", "AZZA3", "SOMA3", "CEAB3",
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
    "RUMO3", "CCRO3", "RAIL3",
    # Agronegócio
    "SLCE3",
    # Indústria & Outros
    "WEGE3", "EMBR3", "TOTS3", "POMO4",
    # Imóveis & Shopping
    "MULT3", "ALLOS3", "IGTI11",
    # Saneamento
    "SBSP3",
    # Petroquímica
    "BRKM5",
    # Seguros & Previdência
    "PSSA3",
    # Diversificado
    "UGPA3", "RAIZ4", "CSAN3", "MRFG3", "BEEF3",
    "NTCO3", "SMFT3", "ALOS3", "TAEE11", "TRPL4",
    "RANI3",
]

# Remove duplicatas mantendo a ordem
seen = set()
TICKERS = [t for t in TICKERS if not (t in seen or seen.add(t))]

# Timeframe principal (contexto)
INTERVALO = "15m"

PERIODO = "5d"

# MÉDIAS

MM_RAPIDA    = 9
MM_LENTA     = 21
MM_TENDENCIA = 21

# SUPORTE / RESISTÊNCIA
JANELA_SR = 20

# VOLUME

# mais seletivo (antes 1.5)
VOLUME_FATOR  = 1.8
VOLUME_JANELA = 20

# HORÁRIO

# evita abertura caótica
HORA_INICIO = "10:05"

# evita final sem liquidez
HORA_FIM = "16:30"

# CONTROLE DE QUALIDADE

# distância máxima da MM9 (1%)
DISTANCIA_MAX = 0.01

# score mínimo
SCORE_MINIMO = 2