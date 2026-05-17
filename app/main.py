import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

INDICATOR_NAMES = {
    "selic": "SELIC",
    "ipca": "IPCA",
    "ipca_habitacao": "IPCA Habitação",
    "incc_di": "INCC-DI",
    "ic_br_metal": "IC-BR Metal",
    "ic_br_metal_usd": "IC-BR Metal (USD)",
    "sinapi": "SINAPI",
    "sinapi_mo": "SINAPI Mão de Obra",
    "sinapi_mat": "SINAPI Materiais",
}

st.set_page_config(
    page_title="Radar de Indicadores — Construção Civil",
    layout="wide",
)

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_parquet(Path("data/gold/indicators.parquet"))
    df["indicator"] = df["indicator"].replace(INDICATOR_NAMES)
    return df

df = load_data()

st.title("Radar de Indicadores — Construção Civil")
st.sidebar.header("Filtros")

available_indicators = sorted(df["indicator"].unique())
selected_indicators = st.sidebar.multiselect(
    "Indicadores",
    options=available_indicators,
    default=available_indicators,
)

ano_min = df["date"].dt.year.min()
ano_max = df["date"].dt.year.max()

ano_inicio, ano_fim = st.sidebar.slider(
    "Período",
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max),
)

metrica = st.sidebar.radio(
    "Visualização",
    options=["var_mensal", "var_acumulada", "var_12m"],
    format_func=lambda x: {
        "var_mensal":    "Variação Mensal",
        "var_acumulada": "Variação Acumulada",
        "var_12m":       "Últimos 12 meses",
    }[x],
)

# Aplica filtros
df_filtrado = df[
    (df["indicator"].isin(selected_indicators)) &
    (df["date"].dt.year >= ano_inicio) &
    (df["date"].dt.year <= ano_fim)
].copy()

# Calcula métrica
if metrica == "var_acumulada":
    df_filtrado["var_acumulada"] = df_filtrado.groupby("indicator")["monthly_change"].cumsum()
    y = "var_acumulada"
elif metrica == "var_12m":
    y = "rolling_12m"
else:
    y = "monthly_change"

LABELS = {
    "date": "Data",
    "indicator": "Indicador",
    "monthly_change": "Variação Mensal (%)",
    "var_acumulada": "Variação Acumulada (%)",
    "rolling_12m": "Últimos 12 meses (%)",
}

fig = px.line(
    df_filtrado,
    x="date",
    y=y,
    color="indicator",
    labels=LABELS,
)

fig.update_layout(
    height=600,
    xaxis_title="Data",
    yaxis_title="Variação (%)",
    legend_title="Indicador",
    hovermode="closest",
)

st.plotly_chart(fig, use_container_width=True)