import pandas as pd
from pathlib import Path

metal_series = ["ic_br_metal", "ic_br_metal_usd"]

sinapi_columns = {
    "geral":     "sinapi",
    "mo":        "sinapi_mo",
    "materiais": "sinapi_mat",
}


def load_silver_bcb(folder: Path) -> pd.DataFrame:
    files = list(folder.glob('*.parquet'))
    dfs = []
    for f in files:
        dfs.append(pd.read_parquet(f))
    return pd.concat(dfs, ignore_index=True)


def transform_gold_bcb(df: pd.DataFrame) -> pd.DataFrame:
    dfs = []
    for serie in df['serie'].unique():
        ds = df[df['serie'] == serie].copy().sort_values('data')

        if serie in metal_series:
            ds['valor'] = ds['valor'].pct_change() * 100

        ds = ds.rename(columns={'data': 'date', 'serie': 'indicator', 'valor': 'monthly_change'})
        ds = ds[['date', 'indicator', 'monthly_change']]
        dfs.append(ds)

    return pd.concat(dfs, ignore_index=True)


def transform_gold_sinapi(df: pd.DataFrame) -> pd.DataFrame:
    dfs = []
    for tipo in df['tipo_custo'].unique():
        ds = df[df['tipo_custo'] == tipo].copy().sort_values('ano_mes')

        ds['monthly_change'] = ds['custo_m2'].pct_change() * 100
        ds['indicator']  = sinapi_columns[tipo]

        ds = ds.rename(columns={'ano_mes': 'date'})
        ds = ds[['date', 'indicator', 'monthly_change']]
        dfs.append(ds)

    return pd.concat(dfs, ignore_index=True)


def run_gold(silver_dir: Path, output_dir: Path) -> pd.DataFrame:
    df_bcb = load_silver_bcb(silver_dir / 'bcb')
    df_sinapi = pd.read_parquet(silver_dir / 'ibge' / 'sinapi.parquet')

    df_gold_bcb = transform_gold_bcb(df_bcb)
    df_gold_sinapi = transform_gold_sinapi(df_sinapi)

    df_gold = pd.concat([df_gold_bcb, df_gold_sinapi], ignore_index=True)
    df_gold['monthly_change'] = df_gold['monthly_change'].round(4)
    df_gold = df_gold.sort_values(['indicator', 'date']).reset_index(drop=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    df_gold.to_parquet(output_dir / 'indicators.parquet', engine='pyarrow')

    print(f"{df_gold['indicator'].nunique()} indicadores | {len(df_gold)} registros")

    return df_gold