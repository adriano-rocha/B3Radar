import csv
import os
from datetime import datetime

ARQUIVO = "trades.csv"

def inicializar_log():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "data", "hora", "ativo", "setup",
                "direcao", "preco_entrada", "resultado"
            ])


def salvar_sinal(ticker, sinal):
    with open(ARQUIVO, mode="a", newline="") as file:
        writer = csv.writer(file)

        agora = datetime.now()

        writer.writerow([
            agora.strftime("%d/%m/%Y"),
            agora.strftime("%H:%M"),
            ticker,
            sinal["setup"],
            sinal["direcao"],
            round(sinal["preco"], 2),
            ""  # resultado vazio por enquanto
        ])