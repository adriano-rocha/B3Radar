import yfinance as yf
from ta.trend import SMAIndicator
from config import (
    INTERVALO, PERIODO, MM_RAPIDA, MM_LENTA,
    JANELA_SR, MM_TENDENCIA, VOLUME_FATOR, VOLUME_JANELA,
    DISTANCIA_MAX, SCORE_MINIMO
)

# timeframe de confirmação
INTERVALO_EXECUCAO = "5m"

# ── DADOS ─────────────────────────────────────────────────────────────────────

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


# ── FILTROS ───────────────────────────────────────────────────────────────────

def filtro_tendencia(df):
    try:
        mm = SMAIndicator(df["Close"], window=MM_TENDENCIA).sma_indicator()
        preco = df["Close"].iloc[-1]
        return "ALTA" if preco > mm.iloc[-1] else "BAIXA"
    except:
        return None


def filtro_volume(df):
    try:
        vol = df["Volume"].iloc[-1]
        media = df["Volume"].iloc[-VOLUME_JANELA - 1:-1].mean()
        return float(vol) >= VOLUME_FATOR * float(media)
    except:
        return False


def volume_direcional(df):
    candle = df.iloc[-1]
    return "COMPRA" if candle["Close"] > candle["Open"] else "VENDA"


def filtro_distancia_media(df):
    """
    Retorna True se o preço NÃO está esticado da MM9.
    Usa DISTANCIA_MAX do config (padrão 1%).
    """
    try:
        mm9 = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()
        preco = float(df["Close"].iloc[-1])
        mm_atual = float(mm9.iloc[-1])
        distancia = abs(preco - mm_atual) / mm_atual
        return distancia < DISTANCIA_MAX
    except:
        # BUG CORRIGIDO: antes retornava False em caso de erro,
        # derrubando o score desnecessariamente
        return True


def confirmar_entrada(ticker, direcao):
    """
    CORRIGIDO: confirmação mais realista.
    Antes exigia fechamento acima da MÁXIMA do candle anterior (muito restritivo).
    Agora exige apenas fechamento acima do FECHAMENTO anterior.
    """
    df = get_dados(ticker, INTERVALO_EXECUCAO)
    if df is None or len(df) < 5:
        # Se não conseguir dados do 5m, não bloqueia o sinal
        return True

    ultimo = df.iloc[-1]
    anterior = df.iloc[-2]

    if direcao == "COMPRA":
        return float(ultimo["Close"]) > float(anterior["Close"])

    if direcao == "VENDA":
        return float(ultimo["Close"]) < float(anterior["Close"])

    return False


# ── SETUPS ────────────────────────────────────────────────────────────────────

def setup_92(df, tendencia):
    """Preço cruza a MM9 a favor da tendência."""
    try:
        mm9 = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()

        f_atual = float(df["Close"].iloc[-1])
        f_ant   = float(df["Close"].iloc[-2])
        mm_atual = float(mm9.iloc[-1])
        mm_ant   = float(mm9.iloc[-2])

        if tendencia == "ALTA" and f_ant < mm_ant and f_atual > mm_atual:
            return "COMPRA"
        if tendencia == "BAIXA" and f_ant > mm_ant and f_atual < mm_atual:
            return "VENDA"
        return None
    except:
        return None


def cruzamento_medias(df, tendencia):
    """MM9 cruza a MM21 a favor da tendência."""
    try:
        mm9  = SMAIndicator(df["Close"], window=MM_RAPIDA).sma_indicator()
        mm21 = SMAIndicator(df["Close"], window=MM_LENTA).sma_indicator()

        if tendencia == "ALTA" and mm9.iloc[-2] < mm21.iloc[-2] and mm9.iloc[-1] > mm21.iloc[-1]:
            return "COMPRA"
        if tendencia == "BAIXA" and mm9.iloc[-2] > mm21.iloc[-2] and mm9.iloc[-1] < mm21.iloc[-1]:
            return "VENDA"
        return None
    except:
        return None


def rompimento_sr(df, tendencia):
    """Preço rompe suporte ou resistência da janela."""
    try:
        janela = df.iloc[-JANELA_SR - 1:-1]
        resistencia = janela["High"].max()
        suporte     = janela["Low"].min()

        f_atual = float(df["Close"].iloc[-1])
        f_ant   = float(df["Close"].iloc[-2])

        if tendencia == "ALTA" and f_ant <= float(resistencia) and f_atual > float(resistencia):
            return "COMPRA", round(float(resistencia), 2)
        if tendencia == "BAIXA" and f_ant >= float(suporte) and f_atual < float(suporte):
            return "VENDA", round(float(suporte), 2)
        return None, None
    except:
        return None, None


# ── SCORE ─────────────────────────────────────────────────────────────────────

def calcular_score(volume_ok, direcao_volume, direcao_sinal, distancia_ok):
    score = 0
    if volume_ok:
        score += 1
    if direcao_volume == direcao_sinal:
        score += 1
    if distancia_ok:
        score += 1
    return score


# ── ANALISAR (entry point) ────────────────────────────────────────────────────

def analisar(ticker):
    df = get_dados(ticker)
    if df is None or len(df) < 30:
        return []

    tendencia = filtro_tendencia(df)
    if tendencia is None:
        return []

    volume_ok      = filtro_volume(df)
    direcao_volume = volume_direcional(df)
    distancia_ok   = filtro_distancia_media(df)
    preco          = round(float(df["Close"].iloc[-1]), 2)
    sinais         = []

    # ── Setup 9.2 ──
    direcao = setup_92(df, tendencia)
    if direcao:
        score = calcular_score(volume_ok, direcao_volume, direcao, distancia_ok)
        if score >= SCORE_MINIMO and confirmar_entrada(ticker, direcao):
            sinais.append({
                "setup": "Setup 9.2",
                "direcao": direcao,
                "preco": preco,
                "nivel": None,
                "tendencia": tendencia
            })

    # ── Cruzamento de Médias ── (BUG CORRIGIDO: estava faltando esta chamada)
    direcao = cruzamento_medias(df, tendencia)
    if direcao:
        score = calcular_score(volume_ok, direcao_volume, direcao, distancia_ok)
        if score >= SCORE_MINIMO and confirmar_entrada(ticker, direcao):
            sinais.append({
                "setup": "Cruzamento MM",
                "direcao": direcao,
                "preco": preco,
                "nivel": None,
                "tendencia": tendencia
            })

    # ── Rompimento S/R ──
    direcao, nivel = rompimento_sr(df, tendencia)
    if direcao:
        score = calcular_score(volume_ok, direcao_volume, direcao, distancia_ok)
        if score >= SCORE_MINIMO and confirmar_entrada(ticker, direcao):
            sinais.append({
                "setup": "Rompimento S/R",
                "direcao": direcao,
                "preco": preco,
                "nivel": nivel,
                "tendencia": tendencia
            })

    return sinais