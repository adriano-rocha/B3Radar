# 📡 B3Radar — Dashboard de Mercado B3

Dashboard interativo para acompanhamento de indicadores da Bolsa de Valores brasileira (B3), construído com Python e Streamlit.

---

## 🖥️ Demonstração

> Exibe em tempo real: IBOVESPA, Dólar, e principais ações como PETR4, VALE3, ITUB4 e BBDC4 — com alertas de preço e exportação de dados.

---

## 🚀 Funcionalidades

- 📈 Cotações ao vivo de IBOV, Dólar, PETR4, VALE3, ITUB4 e BBDC4
- 🔔 Alertas configuráveis de preço por ação
- 📥 Exportação de dados em `.csv` e `.txt`
- 🔄 Atualização manual dos dados com limpeza de cache
- 🔒 API Key protegida via variável de ambiente (`.env`)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| [Python 3](https://python.org) | Linguagem principal |
| [Streamlit](https://streamlit.io) | Interface web interativa |
| [HG Brasil Finance API](https://hgbrasil.com/status/finance) | Dados de mercado em tempo real |
| [Requests](https://pypi.org/project/requests/) | Requisições HTTP |
| [Pandas](https://pandas.pydata.org) | Manipulação de dados |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gerenciamento de variáveis de ambiente |

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

**4. Configure a API Key**

Crie um arquivo `.env` na raiz do projeto:
```
HG_API_KEY=sua_chave_aqui
```

> 🔑 Obtenha sua chave gratuita em [hgbrasil.com/status/finance](https://hgbrasil.com/status/finance). Escolha a opção **"Chave para uso interno"**.

**5. Execute o projeto**
```bash
streamlit run app.py
```

Acesse em: `http://localhost:8501`

---

## 🔐 Segurança

A API Key **nunca** deve ser exposta publicamente. Este projeto utiliza um arquivo `.env` para protegê-la localmente.

O arquivo `.gitignore` já está configurado para ignorar o `.env`:
```
.env
venv/
__pycache__/
```

> ⚠️ Nunca suba sua `.env` para o GitHub.

---

## 📁 Estrutura do Projeto

```
b3radar/
├── app.py              # Aplicação principal
├── .env                # Variáveis de ambiente (não versionar)
├── .gitignore          # Arquivos ignorados pelo Git
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

---

## 📋 requirements.txt

```
streamlit
requests
pandas
python-dotenv
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

Feito por **Adriano Rocha**  
[GitHub](https://github.com/adriano-rocha) · [LinkedIn](https://https://www.linkedin.com/in/adriano-rocha-464044305/)