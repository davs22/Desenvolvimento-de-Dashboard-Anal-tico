# 📊 Desenvolvimento de Dashboard Analítico — Ibovespa

Projeto acadêmico desenvolvido para análise exploratória e visualização de indicadores fundamentalistas de empresas integrantes do **Ibovespa**, utilizando **Python**, **PostgreSQL**, **Docker** e **Power BI**.

O projeto contempla desde a coleta e persistência dos dados até a construção de um modelo dimensional em **Star Schema** e o desenvolvimento de dashboards interativos para análise financeira e histórica das ações.

---

## 🎯 Objetivo

Construir uma solução analítica capaz de:

- coletar dados financeiros e históricos de ações;
- armazenar os dados em um banco PostgreSQL estruturado;
- organizar as informações em um modelo estrela;
- calcular indicadores fundamentalistas;
- comparar o desempenho de empresas do Ibovespa;
- acompanhar a evolução histórica dos preços das ações;
- disponibilizar análises interativas no Power BI.

---

## 🏢 Empresas analisadas

| Ticker | Empresa | Classe |
|---|---|---|
| `VALE3` | Vale | ON |
| `PETR4` | Petrobras | PN |
| `WEGE3` | WEG | ON |
| `ABEV3` | Ambev | ON |
| `RENT3` | Localiza | ON |

O período principal de análise apresentado no dashboard é **2023 a 2025**. Dados financeiros de **2022** também são mantidos no banco para permitir o cálculo do crescimento de receita de 2023.

---

## 📈 Indicadores utilizados

Foram implementados os seguintes indicadores:

- **ROE — Return on Equity**
- **ROA — Return on Assets**
- **Margem Líquida**
- **Crescimento da Receita**
- **Dividend Yield**

Também são utilizadas medidas auxiliares como Receita Líquida, Lucro Líquido, Patrimônio Líquido, Ativo Total, Preço de Referência, Proventos por Ação, Máxima do Período e Mínima do Período.

---

## 🧱 Arquitetura da solução

```text
Yahoo Finance / yfinance
          │
          ▼
       Python
  coleta e tratamento
          │
          ▼
     PostgreSQL
     Star Schema
          │
          ▼
      Power BI
          │
          ▼
 Dashboards Analíticos
```

---

## ⭐ Modelo dimensional

O banco foi estruturado no padrão **Star Schema**.

### Dimensões

- `dim_empresa`
- `dim_data`

### Tabelas fato

- `fato_preco`
- `fato_financeiro`
- `fato_provento`

Estrutura simplificada:

```text
                   dim_empresa
                  /     |      \
                 /      |       \
                ▼       ▼        ▼
         fato_preco fato_financeiro fato_provento
                ▲       ▲        ▲
                 \      |       /
                  \     |      /
                    dim_data
```

---

## 🗄️ Estrutura principal do banco

### `dim_empresa`

```text
empresa_id
ticker
empresa
setor
classe_acao
```

### `dim_data`

```text
data
ano
trimestre
mes_numero
mes
ano_mes
dia
dia_semana
```

### `fato_preco`

```text
data
empresa_id
abertura
maxima
minima
fechamento
preco_ajustado
volume
quantidade_negocios
```

### `fato_financeiro`

```text
data_referencia
ano
empresa_id
receita_liquida
lucro_liquido
lucro_atribuivel_controlador
ativo_total
patrimonio_liquido
lpa
qtd_acoes_vpa
vpa
```

### `fato_provento`

```text
provento_id
data_pagamento
empresa_id
tipo_provento
valor_por_acao
valor_total
```

---

## 🖥️ Dashboards

O relatório do Power BI foi dividido em três páginas.

### 1. Visão Geral

- cartões de indicadores;
- filtros por empresa e ano;
- gráfico de lucro líquido por empresa;
- tabela comparativa de indicadores.

### 2. Indicadores

- evolução do ROE;
- evolução do ROA;
- evolução da Margem Líquida;
- Crescimento da Receita;
- evolução do Dividend Yield.

### 3. Histórico de Preços

A página permite analisar a evolução das ações com drill-down temporal:

```text
Ano
 └── Trimestre
      └── Mês
           └── Dia
```

Também são apresentados Preço de Referência, Máxima do Período e Mínima do Período.

---

## 📊 Volume de dados carregado

| Conjunto | Registros |
|---|---:|
| Histórico de preços | 3.745 |
| Dados financeiros | 20 |
| Proventos | 59 |

O histórico de preços contém aproximadamente **749 pregões por empresa** entre 2023 e 2025.

---

## 🛠️ Tecnologias utilizadas

### Dados e backend

- Python
- Pandas
- yfinance
- Requests
- SQLAlchemy
- Psycopg
- python-dotenv

### Banco de dados

- PostgreSQL 15
- Docker
- Docker Compose

### Business Intelligence

- Microsoft Power BI Desktop
- DAX
- Modelagem dimensional / Star Schema

### Desenvolvimento

- Visual Studio Code
- Git
- GitHub

---

## 📁 Estrutura sugerida do projeto

```text
Desenvolvimento-de-Dashboard-Analitico/
│
├── docker-compose.yml
├── .env
├── requirements.txt
├── init_db.py
├── load_data.py
├── Dashboard_Analitico_Ibovespa.pbix
├── artigo/
│   └── Artigo_Dashboard_Analitico_Ibovespa_Unisales.pdf
└── README.md
```

> O arquivo `.env` não deve ser versionado no GitHub.

---

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/davs22/Desenvolvimento-de-Dashboard-Analitico.git
cd Desenvolvimento-de-Dashboard-Analitico
```

### 2. Criar e ativar o ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

Principais dependências:

```text
pandas
yfinance
requests
SQLAlchemy
psycopg[binary]
python-dotenv
```

### 4. Configurar o `.env`

Exemplo:

```env
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=dashboard_financeiro
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

> Ajuste a porta conforme o mapeamento definido no `docker-compose.yml`.

### 5. Iniciar o PostgreSQL

```bash
docker compose up -d
```

### 6. Criar o modelo de dados

```bash
python init_db.py
```

### 7. Carregar os dados

```bash
python load_data.py
```

---

## 🔌 Conexão com Power BI

No Power BI Desktop:

```text
Obter Dados
→ PostgreSQL
```

Exemplo:

```text
Servidor: 127.0.0.1:5433
Banco: dashboard_financeiro
```

Importe:

```text
dim_empresa
dim_data
fato_preco
fato_financeiro
fato_provento
```

Os relacionamentos seguem cardinalidade **1:N**, partindo das dimensões para as tabelas fato.

---

## 🧮 Exemplos de medidas DAX

### ROE

```DAX
ROE =
DIVIDE(
    [Lucro Líquido],
    [Patrimônio Líquido]
)
```

### ROA

```DAX
ROA =
DIVIDE(
    [Lucro Líquido],
    [Ativo Total]
)
```

### Margem Líquida

```DAX
Margem Líquida =
DIVIDE(
    [Lucro Líquido],
    [Receita Líquida]
)
```

### Dividend Yield

```DAX
Dividend Yield =
DIVIDE(
    [Proventos por Ação],
    [Preço Referência]
)
```

---

## 📚 Contexto acadêmico

Projeto desenvolvido no curso de **Sistemas de Informação** do Centro Universitário Salesiano — Unisales, com aplicação de conceitos de:

- Business Intelligence;
- análise fundamentalista;
- storytelling com dados;
- banco de dados;
- modelagem dimensional;
- indicadores financeiros;
- visualização analítica;
- Power BI.

O projeto também possui artigo acadêmico elaborado conforme o **Guia de Elaboração e Normalização de Trabalhos Acadêmicos e de Pesquisa do Unisales**.

---

## 👥 Autores

**Matheus Diirr Aguiar Veiga de Souza**  
Centro Universitário Salesiano — Unisales  
GitHub: [@davs22](https://github.com/davs22)

**Debora Cupertino de Araújo Lacerda**  
Centro Universitário Salesiano — Unisales

---

## 📄 Licença e aviso

Este projeto foi desenvolvido para fins **acadêmicos e educacionais**.

As informações, indicadores e visualizações apresentadas **não constituem recomendação de compra, venda ou manutenção de ativos financeiros**.
