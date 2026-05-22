# 🏗️ Radar de Indicadores — Construção Civil

Pipeline de dados end-to-end que automatiza a extração, tratamento e consolidação de indicadores econômicos voltados ao setor da construção civil brasileira.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)

## Visão Geral do Projeto

O projeto consiste em um fluxo completo de engenharia de dados que consome dados de duas APIs externas (**Banco Central do Brasil** e **IBGE/SIDRA**), estruturando as informações para análise temporal histórica. 

O processamento e a transformação dos dados seguem a **Arquitetura Medalhão**, garantindo a organização do pipeline desde o dado bruto até a entrega final no dashboard:

* **Fontes:** Ingestão via API do BCB (SGS) e IBGE (SIDRA).
* **Camada Bronze:** Armazenamento dos arquivos JSON brutos exatamente como retornados pelas fontes.
* **Camada Silver:** Limpeza, tipagem forte, tratamento de datas e conversão para o formato colunar Parquet.
* **Camada Gold:** Consolidação das tabelas e cálculo das métricas de variação temporal (mensal, acumulada e últimos 12 meses).
* **Consumo:** Dashboard interativo em Streamlit consumindo o arquivo final otimizado.

---

## Arquitetura

<img width="5100" height="1769" alt="excalidraw_project" src="https://github.com/user-attachments/assets/7e22a8d0-dc99-4df9-a85c-b9eea429ba47" />

---



##  Indicadores

| Indicador | Descrição |
|---|---|
| SELIC | Taxa básica de juros definida pelo Copom. Influencia diretamente o custo de financiamentos imobiliários. |
| IPCA | Índice oficial de inflação do Brasil. Referência para reajustes de contratos e correção monetária. |
| IPCA Habitação | Subgrupo do IPCA focado em habitação, englobando aluguel, condomínio e manutenção residencial, por exemplo. |
| INCC-DI | Índice de custo da construção residencial calculado pela FGV, cobrindo materiais e mão de obra. |
| IC-BR Metal (BRL) | Índice de commodities metálicas em reais. Reflete a variação de preços de minério de ferro, cobre e alumínio convertidos para a moeda nacional. |
| IC-BR Metal (USD) | Mesma cesta do IC-BR Metal em dólares. Permite isolar o efeito cambial nos insumos importados. |
| SINAPI | Custo médio por m² da construção residencial. Referência oficial para orçamentos de obras públicas. |
| SINAPI Materiais | Componente do SINAPI referente ao custo de materiais. |
| SINAPI Mão de Obra | Componente do SINAPI referente ao custo de mão de obra e encargos na construção civil. |

---
## Estrutura do projeto

```
br-construction-indicators-etl/
│
├── app/
│   └── main.py               # Dashboard Streamlit
│
├── data/
│   ├── bronze/               # JSON brutos das APIs
│   ├── silver/               # Parquets intermediários
│   └── gold/                 # Parquet final consolidado
│
├── src/
│   ├── config/
│   │   ├── settings.py       # Series e configurações
│   │   └── logging_config.py # Configuração de logging
│   ├── ingestion/
│   │   ├── bcb.py            # Extração BCB/SGS
│   │   └── ibge.py           # Extração IBGE/SIDRA
│   ├── silver/
│   │   ├── bcb.py            # Transformação Silver BCB
│   │   └── ibge.py           # Transformação Silver IBGE
│   └── gold/
│       └── gold.py           # Consolidação e métricas
│
├── pipeline.py               # Orquestrador do pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

---

## Pré-requisitos

- Python 3.11+
- Docker (opcional)

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/br-construction-indicators-etl.git
cd br-construction-indicators-etl
```

### 2. Instale as dependências

```bash
# Com uv (recomendado):
uv sync

# Com pip:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

```

### 3. Execute o Pipeline

```bash
# Com uv:
uv run python pipeline.py

# Com pip:
python pipeline.py
```

Extrai os indicadores de 2013 até hoje e gera o data/gold/indicators.parquet`.

### 4. Suba o dashboard

**Com Docker (recomendado):**

```bash
docker-compose up -d --build
```

**Sem Docker:**

```bash
streamlit run app/main.py
```

Acesse em **`http://localhost:8501`**

---

## Dashboard

O dashboard oferece três modos de visualização para os indicadores selecionados:
 
- **Variação Mensal** — a variação percentual de cada indicador mês a mês
- **Variação Acumulada** — o acumulado no período selecionado pelo filtro, calculado dinamicamente
- **Últimos 12 Meses** — a soma das variações dos últimos 12 meses

Filtros disponíveis: seleção de indicadores (multiselect) e intervalo de período (slider por ano).

<img width="1827" height="755" alt="Image" src="https://github.com/user-attachments/assets/79348d22-75d8-4703-816d-b4afa00ceda6" />

---

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| Pandas | Transformação dos dados |
| Requests | Extração via API |
| Streamlit | Dashboard interativo |
| Plotly | Visualização de gráficos |
| Docker | Containerização |
| Parquet | Formato de armazenamento |

---
## Autor

**Ramon Marsan Rozas**

- LinkedIn: [https://linkedin.com/in/ramon-m-rozas](https://linkedin.com/in/ramon-m-rozas)
- GitHub: [github.com/rmnrozas](https://github.com/rmnrozas)
