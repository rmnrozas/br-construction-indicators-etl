import pandas as pd
import logging

from pathlib import Path
from src.config.settings import SERIES

def get_latest_file(folder: Path) -> Path:
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