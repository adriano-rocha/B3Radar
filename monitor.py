import time
import requests
import feedparser
from datetime import datetime, timedelta
from setups import analisar
from config import (
    TICKERS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID,
    HORA_INICIO, HORA_FIM, INTERVALO
)

INTERVALO_MINUTOS = 15

# ─────────────────────────────────────────────
# FILTRO PROFISSIONAL DE NOTÍCIAS POR CATEGORIA
# ─────────────────────────────────────────────

# 🥇 1. Dados macro dos EUA — maior impacto global
PALAVRAS_EUA = [
    "payroll", "nonfarm", "fed", "federal reserve", "fomc",
    "juros eua", "taxa americana", "cpi eua", "inflação americana",
    "pib eua", "recessão americana", "powell", "dados americanos",
    "economia americana", "desemprego eua"
]

# 🥈 2. Juros e inflação no Brasil
PALAVRAS_BRASIL_MACRO = [
    "selic", "copom", "banco central", "ipca", "inflação",
    "juros brasil", "taxa básica", "meta de inflação",
    "política monetária", "campos neto", "gabriel galípolo"
]

# 🥉 3. Commodities — petróleo e minério
PALAVRAS_COMMODITIES = [
    "petróleo", "brent", "wti", "crude", "petrobras",
    "minério de ferro", "minério", "vale", "china minério",
    "commodity", "commodities", "opep", "opec"
]

# 🏛️ 4. Política brasileira
PALAVRAS_POLITICA = [
    "lula", "governo federal", "reforma", "gastos públicos",
    "arcabouço fiscal", "déficit", "superávit", "câmara",
    "senado", "congresso", "ministério da fazenda", "haddad",
    "impeachment", "crise política", "teto de gastos"
]

# 💰 5. Balanços e resultados de empresas monitoradas
PALAVRAS_BALANCO = [
    "resultado", "balanço", "lucro", "prejuízo", "receita",
    "ebitda", "guidance", "dividendo", "petrobras resultado",
    "vale resultado", "itaú resultado", "bradesco resultado",
    "wege resultado", "mglu resultado", "bbas resultado"
]

# 🏦 6. Setor bancário e crédito
PALAVRAS_BANCOS = [
    "inadimplência", "crédito", "spread bancário",
    "basileia", "provisão", "sistema financeiro",
    "regulação bancária", "bc regulação"
]

# 🌍 7. China — impacto em commodities
PALAVRAS_CHINA = [
    "china", "crescimento chinês", "pib china", "estímulo chinês",
    "demanda china", "economia china", "banco central chinês",
    "pboc", "xi jinping economia"
]

# ⚡ 8. Eventos inesperados — volatilidade extrema
PALAVRAS_EVENTOS = [
    "guerra", "conflito", "crise", "crash", "colapso",
    "emergência", "calote", "default", "sanção", "recessão",
    "pandemia", "catástrofe", "explosão mercado"
]

# Palavras a IGNORAR — evita notícias irrelevantes
PALAVRAS_IGNORAR = [
    "suécia", "suíça", "japão", "coreia", "austrália",
    "canadá", "méxico", "bolsa europeia", "ftse", "dax",
    "nikkei", "esporte", "futebol", "celebridade", "entretenimento"
]

# Categorias com nome e lista de palavras
CATEGORIAS = [
    ("🥇 EUA/Macro Global", PALAVRAS_EUA),
    ("🥈 Juros/Inflação Brasil", PALAVRAS_BRASIL_MACRO),
    ("🥉 Commodities", PALAVRAS_COMMODITIES),
    ("🏛️ Política Brasileira", PALAVRAS_POLITICA),
    ("💰 Balanços/Resultados", PALAVRAS_BALANCO),
    ("🏦 Setor Bancário", PALAVRAS_BANCOS),
    ("🌍 China", PALAVRAS_CHINA),
    ("⚡ Evento Inesperado", PALAVRAS_EVENTOS),
]

# RSS feeds
RSS_FEEDS = [
    "https://www.infomoney.com.br/feed/",
    "https://br.investing.com/rss/news.rss"
]

# Controle de notícias já enviadas (evita repetição)
noticias_enviadas = set()

# Controle da última hora do resumo enviado
ultima_hora_resumo = None


# ─────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────

def enviar_telegram(mensagem):
    """Envia mensagem pelo bot do Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")


# ─────────────────────────────────────────────
# FORMATAÇÃO DE SINAIS
# ─────────────────────────────────────────────

def formatar_sinal(ticker, sinal):
    """Formata mensagem de sinal de entrada — limpa e direta."""
    emoji_dir = "📈" if sinal["direcao"] == "COMPRA" else "📉"

    msg = (
        f"🔔 <b>SINAL DETECTADO</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>{ticker}</b>\n"
        f"📐 <b>Setup:</b> {sinal['setup']}\n"
        f"{emoji_dir} <b>Direção:</b> {sinal['direcao']}\n"
        f"💰 <b>Preço:</b> R$ {sinal['preco']:.2f}\n"
    )

    if sinal["nivel"]:
        label = "Resistência" if sinal["direcao"] == "COMPRA" else "Suporte"
        msg += f"🎯 <b>{label}:</b> R$ {sinal['nivel']:.2f}\n"

    msg += (
        f"⏰ <b>Horário:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        f"📉 <b>Timeframe:</b> {INTERVALO}"
    )

    return msg


# ─────────────────────────────────────────────
# RESUMO HORÁRIO — IBOV E DÓLAR
# ─────────────────────────────────────────────

def get_ibov():
    try:
        import yfinance as yf
        hist = yf.Ticker("^BVSP").history(period="2d")
        if hist.empty:
            return None
        preco = hist["Close"].iloc[-1]
        anterior = hist["Close"].iloc[-2]
        variacao = ((preco - anterior) / anterior) * 100
        return {"preco": float(preco), "variacao": float(variacao)}
    except Exception:
        return None


def get_dolar():
    try:
        import yfinance as yf
        hist = yf.Ticker("USDBRL=X").history(period="2d")
        if hist.empty:
            return None
        preco = hist["Close"].iloc[-1]
        anterior = hist["Close"].iloc[-2]
        variacao = ((preco - anterior) / anterior) * 100
        return {"preco": float(preco), "variacao": float(variacao)}
    except Exception:
        return None


def enviar_resumo_horario():
    """Envia resumo de IBOV e Dólar na hora cheia."""
    ibov  = get_ibov()
    dolar = get_dolar()

    if ibov is None or dolar is None:
        return

    emoji_ibov  = "📈" if ibov["variacao"] >= 0 else "📉"
    emoji_dolar = "📈" if dolar["variacao"] >= 0 else "📉"

    msg = (
        f"🕐 <b>Resumo de Mercado — {datetime.now().strftime('%H:%M')}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{emoji_ibov} <b>IBOVESPA:</b> {ibov['preco']:,.0f} pts "
        f"({ibov['variacao']:+.2f}%)\n"
        f"{emoji_dolar} <b>Dólar:</b> R$ {dolar['preco']:.2f} "
        f"({dolar['variacao']:+.2f}%)\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📅 {datetime.now().strftime('%d/%m/%Y')}"
    )

    enviar_telegram(msg)
    print(f"  📊 Resumo horário enviado.")


def verificar_resumo_horario():
    """Verifica se está na hora cheia e envia o resumo."""
    global ultima_hora_resumo
    agora = datetime.now()

    if (agora.minute == 0
            and agora.hour >= 11
            and agora.hour <= 17
            and agora.hour != ultima_hora_resumo):
        ultima_hora_resumo = agora.hour
        enviar_resumo_horario()


# ─────────────────────────────────────────────
# NOTÍCIAS IMPACTANTES VIA RSS
# ─────────────────────────────────────────────

def classificar_noticia(titulo):
    """
    Verifica se a notícia é relevante e retorna a categoria.
    Retorna (True, categoria) ou (False, None).
    """
    titulo_lower = titulo.lower()

    # Ignora notícias irrelevantes
    if any(palavra in titulo_lower for palavra in PALAVRAS_IGNORAR):
        return False, None

    # Verifica em qual categoria se encaixa
    for nome_categoria, palavras in CATEGORIAS:
        if any(palavra in titulo_lower for palavra in palavras):
            return True, nome_categoria

    return False, None


def verificar_noticias():
    """Lê RSS dos sites e envia notícias impactantes ainda não enviadas."""
    for url_feed in RSS_FEEDS:
        try:
            feed = feedparser.parse(url_feed)
            for entry in feed.entries[:10]:
                titulo = entry.get("title", "")
                link   = entry.get("link", "")

                if titulo in noticias_enviadas:
                    continue

                relevante, categoria = classificar_noticia(titulo)

                if relevante:
                    noticias_enviadas.add(titulo)
                    fonte = "Infomoney" if "infomoney" in url_feed else "Investing.com"

                    msg = (
                        f"🚨 <b>NOTÍCIA IMPACTANTE</b>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"{categoria}\n"
                        f"📰 {titulo}\n\n"
                        f"🔗 <a href='{link}'>Leia mais</a>\n"
                        f"📡 Fonte: {fonte}\n"
                        f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                    )
                    enviar_telegram(msg)
                    print(f"  🚨 [{categoria}]: {titulo[:60]}...")

        except Exception as e:
            print(f"  Erro ao ler RSS {url_feed}: {e}")


# ─────────────────────────────────────────────
# PREGÃO E SINCRONIZAÇÃO
# ─────────────────────────────────────────────

def dentro_do_pregao():
    agora = datetime.now().strftime("%H:%M")
    return HORA_INICIO <= agora <= HORA_FIM


def proximo_candle():
    agora    = datetime.now()
    abertura = agora.replace(hour=10, minute=0, second=0, microsecond=0)
    segundos_desde_abertura = (agora - abertura).total_seconds()

    if segundos_desde_abertura < 0:
        return abertura

    candles_passados = int(segundos_desde_abertura // (INTERVALO_MINUTOS * 60))
    return abertura + timedelta(minutes=(candles_passados + 1) * INTERVALO_MINUTOS)


def aguardar_proximo_candle():
    proximo = proximo_candle()
    agora   = datetime.now()
    espera  = (proximo - agora).total_seconds()

    if espera <= 0:
        return

    minutos  = int(espera // 60)
    segundos = int(espera % 60)
    print(f"  ⏳ Próximo candle às {proximo.strftime('%H:%M')} — aguardando {minutos}min {segundos}s")
    time.sleep(espera)


# ─────────────────────────────────────────────
# LOOP PRINCIPAL
# ─────────────────────────────────────────────

def verificar_sinais():
    if not dentro_do_pregao():
        print(f"[{datetime.now().strftime('%H:%M')}] Fora do pregão. Aguardando...")
        time.sleep(60)
        return

    print(f"\n[{datetime.now().strftime('%H:%M')}] 🔍 Verificando sinais...")

    for ticker in TICKERS:
        sinais = analisar(ticker)
        if sinais:
            for sinal in sinais:
                msg = formatar_sinal(ticker, sinal)
                enviar_telegram(msg)
                print(f"  ✅ {ticker} — {sinal['setup']} — {sinal['direcao']}")
        else:
            print(f"  — {ticker}: sem sinais")

    verificar_resumo_horario()
    verificar_noticias()


def main():
    print("🚀 B3Radar Monitor iniciado!")
    print(f"📋 Monitorando: {', '.join(TICKERS)}")
    print(f"⏱️  Timeframe: {INTERVALO} | Pregão B3: {HORA_INICIO} às {HORA_FIM}")
    print(f"🔎 Filtros: Tendência MM21 + Volume 1.5x")
    print(f"📰 Notícias: 8 categorias de impacto | Infomoney + Investing.com")
    print("─" * 40)

    enviar_telegram(
        "🚀 <b>B3Radar Monitor iniciado!</b>\n"
        f"📋 Monitorando: {', '.join(TICKERS)}\n"
        f"⏱️ Timeframe: {INTERVALO}\n"
        f"🔎 Filtros: Tendência MM21 + Volume 1.5x\n"
        f"📰 Notícias filtradas por 8 categorias de impacto\n"
        f"🕐 Pregão B3: {HORA_INICIO} às {HORA_FIM}"
    )

    aguardar_proximo_candle()

    while True:
        verificar_sinais()
        if dentro_do_pregao():
            aguardar_proximo_candle()


if __name__ == "__main__":
    main()