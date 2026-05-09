# %%
import pandas as pd
from pathlib import Path

SERIES_INDICE = ["ic_br_metal", "ic_br_metal_usd"]

folder = Path('../../data/silver/bcb')

files = folder.glob('*.parquet')

dfs = []

for f in files:
    df = pd.read_parquet(f)

    dfs.append(df)

df_bcb = pd.concat(dfs, ignore_index=True)

df_bcb

# %%

frames = []

for serie in df_bcb['serie'].unique():
    ds = df_bcb[df_bcb['serie'] == serie].copy().sort_values('data')
    
    if serie in SERIES_INDICE:
        ds['valor'] = ds['valor'].pct_change() * 100
    
    frames.append(ds)

df_bcb = pd.concat(frames, ignore_index=True)

df_bcb

# %%

frames = []

for serie in df_bcb['serie'].unique():
    ds = df_bcb[df_bcb['serie'] == serie].copy().sort_values('data')
    
    ds['var_acumulada'] = ds.groupby(ds['data'].dt.year)['valor'].cumsum()
    ds['var_12m']       = ds['valor'].rolling(12).sum()
    
    frames.append(ds)

df_bcb = pd.concat(frames, ignore_index=True)

df_bcb

# %%

SERIES_INDICE = ["ic_br_metal", "ic_br_metal_usd"]


folder = Path('../../data/silver/bcb')
files = list(folder.glob('*.parquet'))

dfs = []
for f in files:
    df = pd.read_parquet(f)
    dfs.append(df)

df_bcb = pd.concat(dfs, ignore_index=True)

frames_bcb = []
for serie in df_bcb['serie'].unique():
    ds = df_bcb[df_bcb['serie'] == serie].copy().sort_values('data')
    
    if serie in SERIES_INDICE:
        ds['valor'] = ds['valor'].pct_change() * 100
    
    ds = ds.rename(columns={'data': 'date', 'serie': 'indicador', 'valor': 'var_mensal'})
    ds = ds[['date', 'indicador', 'var_mensal']]
    
    frames_bcb.append(ds)

df_gold_bcb = pd.concat(frames_bcb, ignore_index=True)


df_sinapi = pd.read_parquet('../../data/silver/ibge/sinapi.parquet')

sinapi_columns = {
    "geral": "sinapi",
    "mo": "sinapi_mo",
    "materiais": "sinapi_mat",
}

frames_sinapi = []
for tipo in df_sinapi['tipo_custo'].unique():
    ds = df_sinapi[df_sinapi['tipo_custo'] == tipo].copy().sort_values('ano_mes')
    
    ds['var_mensal'] = ds['custo_m2'].pct_change() * 100
    ds['indicador']  = sinapi_columns[tipo]
    
    ds = ds.rename(columns={'ano_mes': 'date'})
    ds = ds[['date', 'indicador', 'var_mensal']]
    
    frames_sinapi.append(ds)

df_gold_sinapi = pd.concat(frames_sinapi, ignore_index=True)


df_gold = pd.concat([df_gold_bcb, df_gold_sinapi], ignore_index=True)
df_gold = df_gold.dropna(subset=['var_mensal']).round(4)
df_gold = df_gold.sort_values(['indicador', 'date']).reset_index(drop=True)

df_gold