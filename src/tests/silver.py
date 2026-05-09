# %%
import pandas as pd

# %%

def transform_sinapi(df: pd.DataFrame):

    # MAPEAMENTO VARIÁVEIS
    # 48 - Custo Geral
    # 2119 - Materiais
    # 2120 - MO

    df = df.drop(['MC', 'NC', 'NN', 'D1C', 'D1N', 'D3N'], axis=1)

    # Transformação colunas 
    new_columns = df.iloc[0]

    df.columns = new_columns

    # Remoção da primeira linha duplicada
    df = df.drop(index=0)

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
        .pct_change() * 100
    )

    return df
# %%

def parse_bcb_series(serie_name: str):

    path = f'../../data/raw/bcb/{serie_name}/20260414_response.json'

    df = pd.read_json(path)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)

    return df
# %%

def parse_metal_series(serie_name: str):

    path = f'../../data/raw/bcb/{serie_name}/20260426_response.json'

    df = pd.read_json(path)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)

    df = df.sort_values(by=['data'])

    df['variacao_mensal'] = df['valor'].pct_change() * 100

    return df