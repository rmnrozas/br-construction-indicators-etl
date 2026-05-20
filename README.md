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

| Indicador | Fonte | Série |
|---|---|---|
| SELIC | BCB/SGS | 4390 |
| IPCA | BCB/SGS | 433 |
| IPCA Habitação | BCB/SGS | 1636 |
| INCC-DI | BCB/SGS | 192 |
| IC-BR Metal | BCB/SGS | 27576 |
| IC-BR Metal (USD) | BCB/SGS | 29040 |
| SINAPI | IBGE/SIDRA | 2296 |
| SINAPI Materiais | IBGE/SIDRA | 2296 |
| SINAPI Mão de Obra | IBGE/SIDRA | 2296 |

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
- [uv](https://github.com/astral-sh/uv)
- Docker (opcional, recomendado)

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/br-construction-indicators-etl.git
cd br-construction-indicators-etl
```

### 2. Instale as dependências

```bash
uv sync
```

### 3. Gere os dados

```bash
uv run python -m pipeline
```

Extrai os indicadores de 2013 até hoje e gera o data/gold/indicators.parquet`.

### 4. Suba o dashboard

**Com Docker (recomendado):**

```bash
docker-compose up -d --build
```

**Sem Docker:**

```bash
uv run streamlit run app/main.py
```

Acesse em **`http://localhost:8501`**

---

## Dashboard

O dashboard oferece três modos de visualização para os indicadores selecionados:
 
- **Variação Mensal** — a variação percentual de cada indicador mês a mês
- **Variação Acumulada** — o acumulado no período selecionado pelo filtro, calculado dinamicamente
- **Últimos 12 Meses** — a soma das variações dos últimos 12 meses

Filtros disponíveis: seleção de indicadores (multiselect) e intervalo de período (slider por ano).

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
