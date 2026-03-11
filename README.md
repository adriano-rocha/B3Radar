# 📡 B3Radar — Dashboard de Mercado B3

Dashboard interativo para acompanhamento de indicadores da Bolsa de Valores brasileira (B3), construído com Python e Streamlit.

---

## 🖥️ Demonstração

> Exibe em tempo real: IBOVESPA, Dólar, e 28 blue chips monitoradas — com alertas de preço, histórico de 30 dias e exportação de dados.

---

## 🚀 Funcionalidades

- 📈 Cotações ao vivo de IBOV, Dólar e 28 blue chips da B3
- 🔥 Top 3 Altas e 📉 Top 3 Baixas do dia
- 📊 Histórico de preço dos últimos 30 dias por ação
- 🔔 Alertas configuráveis de preço por ação
- 📥 Exportação de dados em `.csv` e `.txt`
- 🔄 Atualização manual dos dados com limpeza de cache

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| [Python 3](https://python.org) | Linguagem principal |
| [Streamlit](https://streamlit.io) | Interface web interativa |
| [yfinance](https://pypi.org/project/yfinance/) | Dados de mercado em tempo real (Yahoo Finance) |
| [Pandas](https://pandas.pydata.org) | Manipulação de dados |

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/b3radar.git
cd b3radar
```

**2. Crie e ative um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute o projeto**
```bash
streamlit run app.py
```

Acesse em: `http://localhost:8501`

> ✅ Não é necessária nenhuma API Key. Os dados são obtidos gratuitamente via Yahoo Finance (yfinance).

---

## 📁 Estrutura do Projeto

```
b3radar/
├── app.py              # Aplicação principal
├── .gitignore          # Arquivos ignorados pelo Git
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

---

## 📋 requirements.txt

```
streamlit
pandas
yfinance
```

---

## 🌐 Deploy

O projeto está publicado no Streamlit Cloud. Para fazer o seu próprio deploy:

1. Suba o projeto para um repositório público no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e selecione o arquivo `app.py`
4. Clique em **Deploy**

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

Feito por **Adriano Rocha**  
[GitHub](https://github.com/adriano-rocha) · [LinkedIn](https://www.linkedin.com/in/adriano-rocha-464044305/)