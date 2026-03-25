import yfinance as yf
from ta.trend import SMAIndicator
from config import (
    INTERVALO, PERIODO, MM_RAPIDA, MM_LENTA,
    JANELA_SR, MM_TENDENCIA, VOLUME_FATOR, VOLUME_JANELA
)

# timeframe de execução
INTERVALO_EXECUCAO = "5m"

# DADOS

def get_dados(ticker, intervalo=INTERVALO):
    try:
        df = yf.download(
            ticker + ".SA",
            period=PERIODO,
            interval=intervalo,
            progress=False,
            auto_adjust=True
        )
        if df.empty:
            return None
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        return df
    except Exception:
        return None

# FILTROS PROFISSIONAIS

def filtro_tendencia(df):
    try:
        mm = SMAIndicator(df["Close"], window=MM_TENDENCIA).sma_indicator()
        preco = df["Close"].iloc[-1]
        mm_atual = mm.iloc[-1]

        return "ALTA" if preco > mm_atual else "BAIXA"
    except:
        return None


def filtro_volume(df):
    try:
        vol = df["Volume"].iloc[-1]
        media = df["Volume"].iloc[-VOLUME_JANELA-1:-1].mean()
        return float(vol) >= VOLUME_FATOR * float(media)
    except:
        return False


# volume direcional
def volume_direcional(df):
    candle = df.iloc[-1]
    return "COMPRA" if candle["Close"] > candle["Open"] else "VENDA"


# distância da média (ANTI ESTICADO)
def filtro_distancia_media(df):
    try:
        mm9 = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()
        preco = df["Close"].iloc[-1]
        mm_atual = mm9.iloc[-1]

        distancia = abs(preco - mm_atual) / mm_atual

        return distancia < 0.01  # 1%
    except:
        return False


# confirmação no timeframe menor
def confirmar_entrada(ticker, direcao):
    df = get_dados(ticker, INTERVALO_EXECUCAO)
    if df is None or len(df) < 5:
        return False

    ultimo = df.iloc[-1]
    anterior = df.iloc[-2]

    if direcao == "COMPRA":
        return ultimo["Close"] > anterior["High"]

    if direcao == "VENDA":
        return ultimo["Close"] < anterior["Low"]

    return False

# SETUPS

def setup_92(df, tendencia):
    try:
        mm9 = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()

        f_atual = df["Close"].iloc[-1]
        f_ant = df["Close"].iloc[-2]
        mm_atual = mm9.iloc[-1]
        mm_ant = mm9.iloc[-2]

        if tendencia == "ALTA" and f_ant < mm_ant and f_atual > mm_atual:
            return "COMPRA"

        if tendencia == "BAIXA" and f_ant > mm_ant and f_atual < mm_atual:
            return "VENDA"

        return None
    except:
        return None


def cruzamento_medias(df, tendencia):
    try:
        mm9 = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()
        mm21 = SMAIndicator(df["Close"], window=MM_LENTA).sma_indicator()

        if tendencia == "ALTA" and mm9.iloc[-2] < mm21.iloc[-2] and mm9.iloc[-1] > mm21.iloc[-1]:
            return "COMPRA"

        if tendencia == "BAIXA" and mm9.iloc[-2] > mm21.iloc[-2] and mm9.iloc[-1] < mm21.iloc[-1]:
            return "VENDA"

        return None
    except:
        return None


def rompimento_sr(df, tendencia):
    try:
        janela = df.iloc[-JANELA_SR-1:-1]

        resistencia = janela["High"].max()
        suporte = janela["Low"].min()

        f_atual = df["Close"].iloc[-1]
        f_ant = df["Close"].iloc[-2]

        if tendencia == "ALTA" and f_ant <= resistencia and f_atual > resistencia:
            return "COMPRA", round(float(resistencia), 2)

        if tendencia == "BAIXA" and f_ant >= suporte and f_atual < suporte:
            return "VENDA", round(float(suporte), 2)

        return None, None
    except:
        return None, None

# SCORE (QUALIDADE DO SINAL)

def calcular_score(volume_ok, direcao_volume, direcao_sinal, distancia_ok):
    score = 0

    if volume_ok:
        score += 1

    if direcao_volume == direcao_sinal:
        score += 1

    if distancia_ok:
        score += 1

    return score

# MAIN

def analisar(ticker):
    df = get_dados(ticker)
    if df is None or len(df) < 30:
        return []

    tendencia = filtro_tendencia(df)
    if tendencia is None:
        return []

    volume_ok = filtro_volume(df)
    direcao_volume = volume_direcional(df)
    distancia_ok = filtro_distancia_media(df)

    preco = round(float(df["Close"].iloc[-1]), 2)
    sinais = []

    # ── SETUP 9.2 ──
    direcao = setup_92(df, tendencia)
    if direcao:
        score = calcular_score(volume_ok, direcao_volume, direcao, distancia_ok)

        if score >= 2 and confirmar_entrada(ticker, direcao):
            sinais.append({
                "setup": "Setup 9.2",
                "direcao": direcao,
                "preco": preco,
                "nivel": None,
                "tendencia": tendencia
            })

    # ── ROMPIMENTO ──
    direcao, nivel = rompimento_sr(df, tendencia)
    if direcao:
        score = calcular_score(volume_ok, direcao_volume, direcao, distancia_ok)

        if score >= 2 and confirmar_entrada(ticker, direcao):
            sinais.append({
                "setup": "Rompimento S/R",
                "direcao": direcao,
                "preco": preco,
                "nivel": nivel,
                "tendencia": tendencia
            })

    return sinais