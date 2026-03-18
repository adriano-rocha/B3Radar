import yfinance as yf
from ta.trend import SMAIndicator
from config import (
    INTERVALO, PERIODO, MM_RAPIDA, MM_LENTA,
    JANELA_SR, MM_TENDENCIA, VOLUME_FATOR, VOLUME_JANELA
)


def get_dados(ticker):
    """Baixa dados do ticker via yfinance."""
    try:
        df = yf.download(
            ticker + ".SA",
            period=PERIODO,
            interval=INTERVALO,
            progress=False,
            auto_adjust=True
        )
        if df.empty:
            return None
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        return df
    except Exception:
        return None


def filtro_tendencia(df):
    """
    Retorna 'ALTA' se preço atual está acima da MM de tendência,
    'BAIXA' se está abaixo.
    """
    try:
        mm = SMAIndicator(df["Close"], window=MM_TENDENCIA).sma_indicator()
        preco_atual = df["Close"].iloc[-1]
        mm_atual    = mm.iloc[-1]

        if preco_atual > mm_atual:
            return "ALTA"
        else:
            return "BAIXA"
    except Exception:
        return None


def filtro_volume(df):
    """
    Retorna True se o volume do candle atual é >= VOLUME_FATOR x média dos últimos N candles.
    """
    try:
        volume_atual  = df["Volume"].iloc[-1]
        media_volume  = df["Volume"].iloc[-VOLUME_JANELA-1:-1].mean()
        return float(volume_atual) >= VOLUME_FATOR * float(media_volume)
    except Exception:
        return False


def setup_92(df, tendencia):
    """
    Setup 9.2 — Candle fecha acima da MM9 após ficar abaixo (compra)
    ou fecha abaixo da MM9 após ficar acima (venda).
    Filtrado pela tendência: só COMPRA em alta, só VENDA em baixa.
    """
    try:
        mm9 = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()

        fechamento_atual    = df["Close"].iloc[-1]
        fechamento_anterior = df["Close"].iloc[-2]
        mm9_atual           = mm9.iloc[-1]
        mm9_anterior        = mm9.iloc[-2]

        if (tendencia == "ALTA"
                and fechamento_anterior < mm9_anterior
                and fechamento_atual > mm9_atual):
            return "COMPRA"

        if (tendencia == "BAIXA"
                and fechamento_anterior > mm9_anterior
                and fechamento_atual < mm9_atual):
            return "VENDA"

        return None
    except Exception:
        return None


def cruzamento_medias(df, tendencia):
    """
    Cruzamento MM9 x MM21.
    Só COMPRA em tendência de alta, só VENDA em tendência de baixa.
    """
    try:
        mm9  = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()
        mm21 = SMAIndicator(df["Close"], window=MM_LENTA).sma_indicator()

        if (tendencia == "ALTA"
                and mm9.iloc[-2] < mm21.iloc[-2]
                and mm9.iloc[-1] > mm21.iloc[-1]):
            return "COMPRA"

        if (tendencia == "BAIXA"
                and mm9.iloc[-2] > mm21.iloc[-2]
                and mm9.iloc[-1] < mm21.iloc[-1]):
            return "VENDA"

        return None
    except Exception:
        return None


def rompimento_sr(df, tendencia):
    """
    Rompimento de suporte/resistência filtrado pela tendência.
    """
    try:
        janela = df.iloc[-JANELA_SR-1:-1]

        resistencia = janela["High"].max()
        suporte     = janela["Low"].min()

        fechamento_atual    = df["Close"].iloc[-1]
        fechamento_anterior = df["Close"].iloc[-2]

        if (tendencia == "ALTA"
                and fechamento_anterior <= resistencia
                and fechamento_atual > resistencia):
            return "COMPRA", round(float(resistencia), 2)

        if (tendencia == "BAIXA"
                and fechamento_anterior >= suporte
                and fechamento_atual < suporte):
            return "VENDA", round(float(suporte), 2)

        return None, None
    except Exception:
        return None, None


def analisar(ticker):
    """
    Analisa o ticker e retorna lista de sinais encontrados.
    Aplica filtros de tendência e volume antes de confirmar o sinal.
    """
    df = get_dados(ticker)
    if df is None or len(df) < 30:
        return []

    # ── Filtros globais ──────────────────────
    tendencia = filtro_tendencia(df)
    if tendencia is None:
        return []

    volume_ok = filtro_volume(df)
    if not volume_ok:
        return []
    # ────────────────────────────────────────

    preco_atual = round(float(df["Close"].iloc[-1]), 2)
    sinais = []

    # Setup 9.2
    resultado_92 = setup_92(df, tendencia)
    if resultado_92:
        sinais.append({
            "setup":    "Setup 9.2",
            "direcao":  resultado_92,
            "preco":    preco_atual,
            "nivel":    None,
            "tendencia": tendencia
        })

    # Cruzamento de médias
    resultado_mm = cruzamento_medias(df, tendencia)
    if resultado_mm:
        sinais.append({
            "setup":    "Cruzamento MM9 x MM21",
            "direcao":  resultado_mm,
            "preco":    preco_atual,
            "nivel":    None,
            "tendencia": tendencia
        })

    # Rompimento S/R
    resultado_sr, nivel = rompimento_sr(df, tendencia)
    if resultado_sr:
        sinais.append({
            "setup":    "Rompimento de Suporte/Resistência",
            "direcao":  resultado_sr,
            "preco":    preco_atual,
            "nivel":    nivel,
            "tendencia": tendencia
        })

    return sinais