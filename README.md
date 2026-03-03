# 📊 B3 Radar

Aplicação Streamlit para monitoramento em tempo real do Ibovespa e ações da B3.

## 🚀 Funcionalidades

- ✅ Cotação atual do Ibovespa (^BVSP)
- ✅ Dados históricos com gráficos
- ✅ Atualização automática a cada 2 minutos
- ✅ Interface intuitiva com Streamlit

## 🛠️ Tecnologias

- Python 3.x
- Streamlit
- yfinance
- pandas

## 📋 Pré-requisitos

- Python 3.8+
- pip

## 🔧 Instalação

1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/b3radar.git
cd b3radar
```

2. Crie e ative o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute a aplicação
```bash
streamlit run app.py
```

5. Acesse: http://localhost:8501

## 📁 Estrutura do Projeto
```
b3radar/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
├── README.md          # Documentação
├── .gitignore         # Arquivos ignorados
└── venv/              # Ambiente virtual (não commitado)
```

## 🎯 Uso

A aplicação carrega automaticamente os dados do Ibovespa e atualiza a cada 2 minutos. 

Informações exibidas:
- Valor atual de fechamento
- Período dos dados (últimos 5 dias)
- Status de carregamento

## 📈 Próximas Melhorias

- [ ] Adicionar mais índices (IFIX, SMLL, etc)
- [ ] Gráficos interativos
- [ ] Análise de ações individuais
- [ ] Alertas de preço

## 👤 Autor

**Adriano Rocha**
- GitHub: [@adriano-rocha](https://github.com/adriano-rocha)

## 📝 Licença

Este projeto está sob licença MIT.