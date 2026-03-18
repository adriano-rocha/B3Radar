# ─────────────────────────────────────────────
# CONFIGURAÇÕES DO BOT E MONITORAMENTO
# ─────────────────────────────────────────────

# Telegram
TELEGRAM_TOKEN   = "8726086318:AAHddpAwY-RPJwXak8N6UxQfcy9IZYFURmA"
TELEGRAM_CHAT_ID = "8233791045"

# Tickers para monitorar
TICKERS = ["PETR4", "VALE3", "ITUB4", "BBDC4", "WEGE3", "BBAS3"]

# Intervalo do gráfico
INTERVALO = "15m"

# Período de análise
PERIODO = "5d"

# Parâmetros dos setups
MM_RAPIDA        = 9     # Média móvel rápida
MM_LENTA         = 21    # Média móvel lenta
JANELA_SR        = 20    # Janela para suporte/resistência

# Filtro de tendência
MM_TENDENCIA     = 21    # Preço acima → tendência de alta → só COMPRA
                         # Preço abaixo → tendência de baixa → só VENDA

# Filtro de volume
VOLUME_FATOR     = 1.5   # Volume atual deve ser X vezes a média
VOLUME_JANELA    = 20    # Média de quantos candles para comparar

# Horário do pregão B3
# Pregão contínuo: 10:00 às 17:55
# Leilão de fechamento: 17:55 às 18:00
HORA_INICIO = "10:00"
HORA_FIM    = "17:55"

# Minuto de início do pregão (usado para sincronizar candles)
# Os candles de 15min viram em: 10:00, 10:15, 10:30...
MINUTO_ABERTURA = 0   # minuto da hora de abertura (10:00 → 0)