import time
import requests
import feedparser
from logger import salvar_sinal, inicializar_log
from datetime import datetime, timedelta
from setups import analisar
from config import (
    TICKERS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID,
    HORA_INICIO, HORA_FIM, INTERVALO
)

# CONTROLES GLOBAIS

INTERVALO_MINUTOS = 15
ULTIMO_SINAL = {}
BLOQUEIO_NOTICIA_ATE = None
noticias_enviadas = set()
ultima_hora_resumo = None


# TELEGRAM

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Erro Telegram: {e}")

# IBOV

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
    except:
        return None

# FILTROS PROFISSIONAIS

def dentro_do_pregao():
    agora = datetime.now().strftime("%H:%M")
    return HORA_INICIO <= agora <= HORA_FIM


def horario_operavel():
    agora = datetime.now()
    if 12 <= agora.hour < 14:
        return False
    return True


def direcao_mercado():
    ibov = get_ibov()
    if ibov is None:
        return None

    if ibov["variacao"] > 0.3:
        return "ALTA"
    elif ibov["variacao"] < -0.3:
        return "BAIXA"
    else:
        return "LATERAL"


def validar_direcao(sinal, direcao_ibov):
    if direcao_ibov is None or direcao_ibov == "LATERAL":
        return True

    if direcao_ibov == "ALTA" and sinal["direcao"] == "VENDA":
        return False

    if direcao_ibov == "BAIXA" and sinal["direcao"] == "COMPRA":
        return False

    return True

# BLOQUEIO POR NOTÍCIA

def ativar_bloqueio_noticia():
    global BLOQUEIO_NOTICIA_ATE
    BLOQUEIO_NOTICIA_ATE = datetime.now() + timedelta(minutes=5)


def bloqueio_ativo():
    global BLOQUEIO_NOTICIA_ATE
    if BLOQUEIO_NOTICIA_ATE is None:
        return False
    return datetime.now() < BLOQUEIO_NOTICIA_ATE


def verificar_noticias():
    global noticias_enviadas

    RSS_FEEDS = [
        "https://www.infomoney.com.br/feed/",
        "https://br.investing.com/rss/news.rss"
    ]

    PALAVRAS_IMPORTANTES = [
        "payroll", "fed", "juros", "selic", "inflação",
        "petróleo", "vale", "china", "guerra", "crise"
    ]

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:
                titulo = entry.get("title", "")

                if titulo in noticias_enviadas:
                    continue

                if any(p in titulo.lower() for p in PALAVRAS_IMPORTANTES):
                    noticias_enviadas.add(titulo)

                    ativar_bloqueio_noticia()

                    msg = (
                        f"🚨 NOTÍCIA IMPORTANTE\n"
                        f"{titulo}\n\n"
                        f"⛔ Operações pausadas por 5 min"
                    )

                    enviar_telegram(msg)
                    print(f"🚨 {titulo}")

        except Exception as e:
            print(f"Erro RSS: {e}")


# CONTROLE DE REPETIÇÃO

def pode_enviar_sinal(ticker, sinal):
    chave = f"{ticker}_{sinal['setup']}_{sinal['direcao']}"

    if ULTIMO_SINAL.get(ticker) == chave:
        return False

    ULTIMO_SINAL[ticker] = chave
    return True

# FORMATAÇÃO

def formatar_sinal(ticker, sinal):
    emoji = "📈" if sinal["direcao"] == "COMPRA" else "📉"

    return (
        f"{emoji} {ticker}\n"
        f"{sinal['setup']} | {sinal['direcao']}\n"
        f"R$ {sinal['preco']:.2f}"
    )

# LOOP PRINCIPAL

def verificar_sinais():
    if not dentro_do_pregao():
        print("Fora do pregão...")
        time.sleep(60)
        return

    if not horario_operavel():
        print("Horário ruim...")
        return

    if bloqueio_ativo():
        print("Bloqueado por notícia...")
        return

    direcao_ibov = direcao_mercado()

    print(f"\n[{datetime.now().strftime('%H:%M')}] Verificando...")

    for ticker in TICKERS:
        sinais = analisar(ticker)

        for sinal in sinais:

            if not validar_direcao(sinal, direcao_ibov):
                continue

            if not pode_enviar_sinal(ticker, sinal):
                continue

            msg = formatar_sinal(ticker, sinal)
            enviar_telegram(msg)

            salvar_sinal(ticker, sinal)

            print(f"✅ {ticker} {sinal['direcao']}")


def aguardar_proximo_candle():
    time.sleep(INTERVALO_MINUTOS * 60)


def main():
    print("🚀 BOT INICIADO")

    inicializar_log()

    while True:
        verificar_sinais()
        verificar_noticias()
        aguardar_proximo_candle()


if __name__ == "__main__":
    main()