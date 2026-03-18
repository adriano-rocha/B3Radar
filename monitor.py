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

PALAVRAS_CHAVE = [
    "selic", "fed", "federal reserve", "juros", "inflação", "ipca",
    "crise", "recessão", "guerra", "sanção", "petróleo", "dólar",
    "ibovespa", "bolsa", "pib", "desemprego", "copom", "banco central",
    "default", "calote", "colapso", "emergência", "queda", "crash"
]

RSS_FEEDS = [
    "https://www.infomoney.com.br/feed/",
    "https://br.investing.com/rss/news.rss"
]

noticias_enviadas = set()

ultima_hora_resumo = None

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

# Resumo IBOV por hora
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
    # Hora cheia dentro do pregão (11:00, 12:00... 17:00)
    if (agora.minute == 0
            and agora.hour >= 11
            and agora.hour <= 17
            and agora.hour != ultima_hora_resumo):
        ultima_hora_resumo = agora.hour
        enviar_resumo_horario()

# Noticias Impactantes

def e_noticia_impactante(titulo):
    """Verifica se o título da notícia contém palavras-chave de impacto."""
    titulo_lower = titulo.lower()
    return any(palavra in titulo_lower for palavra in PALAVRAS_CHAVE)


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

                if e_noticia_impactante(titulo):
                    noticias_enviadas.add(titulo)
                    fonte = "Infomoney" if "infomoney" in url_feed else "Investing.com"

                    msg = (
                        f"🚨 <b>NOTÍCIA IMPACTANTE</b>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📰 {titulo}\n\n"
                        f"🔗 <a href='{link}'>Leia mais</a>\n"
                        f"📡 Fonte: {fonte}\n"
                        f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                    )
                    enviar_telegram(msg)
                    print(f"  🚨 Notícia enviada: {titulo[:60]}...")

        except Exception as e:
            print(f"  Erro ao ler RSS {url_feed}: {e}")


 #Sinc do Pregão
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

    # Verifica resumo horário
    verificar_resumo_horario()

    # Verifica notícias impactantes
    verificar_noticias()

def main():
    print("🚀 B3Radar Monitor iniciado!")
    print(f"📋 Monitorando: {', '.join(TICKERS)}")
    print(f"⏱️  Timeframe: {INTERVALO} | Pregão B3: {HORA_INICIO} às {HORA_FIM}")
    print(f"🔎 Filtros: Tendência MM21 + Volume 1.5x")
    print(f"📰 Notícias: Infomoney + Investing.com")
    print("─" * 40)

    enviar_telegram(
        "🚀 <b>B3Radar Monitor iniciado!</b>\n"
        f"📋 Monitorando: {', '.join(TICKERS)}\n"
        f"⏱️ Timeframe: {INTERVALO}\n"
        f"🔎 Filtros: Tendência MM21 + Volume 1.5x\n"
        f"📰 Notícias em tempo real ativadas\n"
        f"🕐 Pregão B3: {HORA_INICIO} às {HORA_FIM}"
    )

    aguardar_proximo_candle()

    while True:
        verificar_sinais()
        if dentro_do_pregao():
            aguardar_proximo_candle()


if __name__ == "__main__":
    main()