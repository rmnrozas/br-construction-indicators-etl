from datetime import datetime
from pathlib import Path

import time
import requests
import json
import logging

def fetch_bcb(code: int, start_date: str, end_date: str, fmt='json', retries=3):
    
    base_url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados'
    
    params = {
        'formato': fmt,
        'dataInicial': start_date,
        'dataFinal': end_date
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url=base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                logging.info(f"Dados da série {code} obtidos com sucesso na tentativa {attempt}.")
                return response.json()
            
            logging.warning(f"Tentativa {attempt}/{retries} falhou (Status: {response.status_code}). Aguardando 5s...")
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro de comunicação na tentativa {attempt}: {e}")

        time.sleep(5)

    logging.critical(f"Falha : Não foi possível obter a série {code} após {retries} tentativas.")
    response.raise_for_status()

def save_raw_bcb(file_name: str, data: list[dict]):
    raw_dir = Path(f"data/bronze/bcb/{file_name}")
    raw_dir.mkdir(parents=True, exist_ok=True)

    current_date = datetime.today().strftime("%Y%m%d")
    raw_path = raw_dir / f"{current_date}_response.json"

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"Arquivo {file_name}: {len(data)} registros, salvos em {raw_path}")
    return raw_path

def extract_bcb_series(start_date: str, end_date: str, bcb_series: dict):

    for CODE, NAME in bcb_series.items():
        try:
            data = fetch_bcb(code=CODE, start_date=start_date, end_date=end_date)

            if data:
                save_raw_bcb(file_name=NAME, data=data)
            
            else:
                logging.warning(f'Nenhum dado encontrado para {NAME}!')

        except Exception as e:
            logging.error(f'Falha ao extrair {NAME}: {e}')