import pandas as pd
import logging

from pathlib import Path

def get_latest_file(folder: Path):
    files = sorted(folder.glob('*.json'))
    if not files:
        logging.warning(f'Nenhum arquivo JSON encontrado em: {folder}')
        raise FileNotFoundError(f'Nenhum arquivo encontrado em {folder}')
    
    latest_file = files[-1]
    
    return latest_file

def load_bronze_file(folder: Path):

    raw_path = get_latest_file(folder)
    df = pd.read_json(raw_path)

    return df

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

    # Remoção de colunas
    df = df.drop(['Unidade de Medida', 'Variável'], axis=1)

    # Mapeamento variáveis
    df['Variável (Código)'] = df['Variável (Código)'].replace(
        {
            '48' : 'geral',
            '2119' : 'materiais',
            '2120' : 'mo'
        }
    )

    # Renomear colunas
    df = df.rename(columns={
            'Valor': 'custo_m2',
            'Variável (Código)' : 'tipo_custo',
            'Mês (Código)' : 'ano_mes'
        }
    )

    # Alteração de tipos
    df['custo_m2'] = pd.to_numeric(df['custo_m2'], errors='coerce')
    df['ano_mes'] = pd.to_datetime(df['ano_mes'], format='%Y%m')
    logging.info(f"Dados do SINAPI tratados com sucesso!")

    return df

def run_silver_ibge(output_dir: Path = Path("data/silver/ibge"), file_name: str = 'sinapi.parquet'):

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = f'{output_dir}\{file_name}'

    df_bronze = load_bronze_file(folder=Path("data/bronze/ibge/sinapi"))
    df_silver = transform_sinapi(df=df_bronze)

    df_silver.to_parquet(output_path, engine='pyarrow')
    logging.info(f"Dados do SINAPI salvos em {output_path}")


# df = load_bronze_file(Path("data/bronze/ibge/sinapi"))
# transform_sinapi(df=df, output_path=Path("data/silver/ibge/sinapi.parquet"))

#def save_silver_file():



# df = df.sort_values(['tipo_custo', 'ano_mes'])

#     df['variacao_mensal'] = (
#         df.groupby(by=['tipo_custo'])['custo_m2']
#         .pct_change() * 100
#     )