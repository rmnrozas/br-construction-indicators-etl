import logging

from pathlib import Path
from datetime import datetime

from src.ingestion.bcb import extract_bcb_series
from src.ingestion.ibge import extract_sinapi_data

from src.silver.bcb import run_silver_bcb
from src.silver.ibge import run_silver_ibge

from src.gold.gold import run_gold

from src.config.settings import SINAPI_CONFIG, SERIES
from src.config.logging_config import setup_logging

setup_logging()

START_DATE = "01/01/2013"
END_DATE = datetime.today().strftime("%d/%m/%Y")

def run_pipeline():

    logging.info("---------BRONZE---------")
    extract_bcb_series(start_date=START_DATE, end_date=END_DATE,bcb_series=SERIES)
    extract_sinapi_data(start_date=START_DATE, end_date=END_DATE, sinapi_config=SINAPI_CONFIG)

    logging.info("---------SILVER---------")
    run_silver_bcb()
    run_silver_ibge()

    logging.info("---------GOLD---------")
    run_gold(
        silver_dir=Path("data/silver"),
        output_dir=Path("data/gold"),
    )

    logging.info("Pipeline concluído com sucesso.")

if __name__ == "__main__":
    run_pipeline()