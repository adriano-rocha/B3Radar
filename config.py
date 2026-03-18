TELEGRAM_TOKEN   = "8726086318:AAHddpAwY-RPJwXak8N6UxQfcy9IZYFURmA"
TELEGRAM_CHAT_ID = "8233791045"

TICKERS = ["PETR4", "VALE3", "ITUB4", "BBDC4", "WEGE3", "BBAS3"]

INTERVALO = "15m"

PERIODO = "5d"

# Parâmetros dos setups
MM_RAPIDA        = 9     
MM_LENTA         = 21    
JANELA_SR        = 20    # Janela para suporte/resistência

# Filtro de tendência
MM_TENDENCIA     = 21    # Preço acima → tendência de alta → só COMPRA
                         # Preço abaixo → tendência de baixa → só VENDA

# Filtro de volume
VOLUME_FATOR     = 1.5   # Volume atual deve ser X vezes a média
VOLUME_JANELA    = 20    # Média de quantos candles para comparar

HORA_INICIO = "10:00"
HORA_FIM    = "17:55"

MINUTO_ABERTURA = 0  