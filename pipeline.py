import logging

from datetime import datetime

from src.config.settings import SINAPI_CONFIG, SERIES
from src.config.logging_config import setup_logging

from src.ingestion.bcb import BCBIngestor
from src.ingestion.ibge import SINAPIIngestor

from src.silver.bcb import run_silver_bcb
from src.silver.ibge import run_silver_ibge

from src.gold.gold import run_gold

setup_logging()

START_DATE = "01/01/2013"
END_DATE = datetime.today().strftime("%d/%m/%Y")

bcb_ingestor = BCBIngestor(start_date=START_DATE, end_date=END_DATE)
sinapi_ingestor = SINAPIIngestor(start_date=START_DATE, end_date=END_DATE)

def run_pipeline():

    logging.info("---------BRONZE---------")
    bcb_ingestor.extract_bcb(bcb_series=SERIES)
    sinapi_ingestor.extract_sinapi(sinapi_config=SINAPI_CONFIG)

    logging.info("---------SILVER---------")
    run_silver_bcb()
    run_silver_ibge()

    logging.info("---------GOLD---------")
    run_gold()

    logging.info("Pipeline concluído com sucesso.")

if __name__ == "__main__":
    run_pipeline()