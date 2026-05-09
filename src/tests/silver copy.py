# %%

import pandas as pd

# %%

df_raw = pd.read_parquet('../../data/bronze/sinapi.parquet')

df_raw.head()

# %%
# MAPEAMENTO VARIÁVEIS
# 48 Custo Geral
# 2119 Materiais
# 2120 MO

df = df_raw.copy()

df = df.drop(['Unidade de Medida', 'Variável'], axis=1)

df['Variável (Código)'] = df['Variável (Código)'].replace(
    {
        '48' : 'geral',
        '2119' : 'materiais',
        '2120' : 'mo'
    }
)

df = df.rename(columns={
        'Valor': 'custo_m2',
        'Variável (Código)' : 'tipo_custo',
        'Mês (Código)' : 'ano_mes'
    }
)

df['custo_m2'] = pd.to_numeric(df['custo_m2'], errors='coerce')
df['ano_mes'] = pd.to_datetime(df['ano_mes'], format='%Y%m')

df = df.dropna(subset=['custo_m2'])

df = df.sort_values(['tipo_custo', 'ano_mes'])

df['variacao_mensal'] = (
    df.groupby(by=['tipo_custo'])['custo_m2']
      .pct_change()
)

#df['custo_m2'] = df['custo_m2'].astype(float)
# %%
df_geral = df[df['tipo_custo'] == 'mo']

df_geral.head()

# %%

def parse_bcb_series(serie_name: str):

    path = f'../../data/raw/bcb/{serie_name}/20260414_response.json'

    df = pd.read_json(path)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)

    return df


#def load_silver_file()

df_incc = parse_bcb_series(serie_name='incc')
df_incc

# %%

# %%

def parse_metal_series(serie_name: str):

    path = f'../../data/raw/bcb/{serie_name}/20260426_response.json'

    df = pd.read_json(path)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)

    df = df.sort_values(by=['data'])

    df['variacao_mensal'] = df['valor'].pct_change() * 100

    return df

# %%

path = f'../../data/raw/bcb/ic_br_metal/20260426_response.json'

df_metal = pd.read_json(path)

df_metal['data'] = pd.to_datetime(df_metal['data'], dayfirst=True)

df_metal = df_metal.sort_values(by=['data'])

df_metal['variacao_mensal'] = df_metal['valor'].pct_change() * 100

df_metal

# %%

df_metal_br = parse_metal_series('ic_br_metal_usd')

df_metal_br