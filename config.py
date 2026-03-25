TELEGRAM_TOKEN   = "SEU_TOKEN"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID"

# Ativos com melhor comportamento técnico
TICKERS = ["PETR4", "VALE3", "ITUB4", "BBDC4", "BBAS3"]

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

# score mínimo (se quiser usar depois)
SCORE_MINIMO = 2