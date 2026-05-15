import logging

from pathlib import Path
from datetime import datetime

from src.ingestion.bcb import extract_bcb_series
from src.ingestion.ibge import extract_sinapi_data
from src.silver.bcb import run_silver_bcb
from src.silver.ibge import load_bronze_file, transform_sinapi
from src.gold.gold import run_gold

from src.config.api_settings import SINAPI_CONFIG, SERIES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

START_DATE = "01/01/2013"
END_DATE   = datetime.today().strftime("%d/%m/%Y")

def run_pipeline():

    logging.info("---------BRONZE---------")
    extract_bcb_series(start_date=START_DATE, end_date=END_DATE,bcb_series=SERIES)
    extract_sinapi_data(start_date=START_DATE, end_date=END_DATE, sinapi_config=SINAPI_CONFIG)

    logging.info("---------SILVER---------")
    run_silver_bcb()
    df_sinapi = load_bronze_file(Path("data/bronze/ibge/sinapi"))
    transform_sinapi(df_sinapi, output_path=Path("data/silver/ibge/sinapi.parquet"))

    logging.info("---------GOLD---------")
    run_gold(
        silver_dir=Path("data/silver"),
        output_dir=Path("data/gold"),
    )

    logging.info("Pipeline concluído com sucesso.")

if __name__ == "__main__":
    run_pipeline()