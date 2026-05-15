import pandas as pd
import logging

from pathlib import Path
from src.config.api_settings import SERIES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_latest_file(folder: Path) -> Path:
    files = sorted(folder.glob('*.json'))
    if not files:
        raise FileNotFoundError(f'Nenhum arquivo encontrado em {folder}')
    return files[-1]


def load_bronze_file(folder: Path):
    raw_path = get_latest_file(folder)
    df = pd.read_json(raw_path)
    return df


def transform_bcb(df: pd.DataFrame, serie_name: str):
    df['data']  = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['serie'] = serie_name
    df = df.dropna(subset=['valor']).sort_values('data').reset_index(drop=True)
    logging.info(f"{serie_name} tratado com sucesso!")
    return df


def run_silver_bcb(output_dir: Path = Path("data/silver/bcb")):
    output_dir.mkdir(parents=True, exist_ok=True)

    for code, name in SERIES.items():
        df = load_bronze_file(Path(f"data/bronze/bcb/{name}"))
        df = transform_bcb(df, serie_name=name)
        df.to_parquet(output_dir / f"{name}.parquet", engine="pyarrow")
        logging.info(f"{name}.parquet salvo em {output_dir}")

#run_silver_bcb()

# def parse_bcb_series(serie_name: str):

#     path = f'../../data/raw/bcb/{serie_name}/20260414_response.json'

#     df = pd.read_json(path)

#     df['data'] = pd.to_datetime(df['data'], dayfirst=True)

#     return df

# def parse_metal_series(serie_name: str):

#     path = f'../../data/raw/bcb/{serie_name}/20260426_response.json'

#     df = pd.read_json(path)

#     df['data'] = pd.to_datetime(df['data'], dayfirst=True)

#     df = df.sort_values(by=['data'])

#     return df


#   df['variacao_mensal'] = df['valor'].pct_change() * 100