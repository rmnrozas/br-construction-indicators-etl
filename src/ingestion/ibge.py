from datetime import datetime
from pathlib import Path

import requests
import json
import time
import logging

def build_sinapi_url(config: dict, start_date: str, end_date: str):
    """
    Monta a URL da API do SIDRA formatando as datas para YYYYMM.

    Espera datas no formato 'DD/MM/YYYY'.
    """
    dt_start = datetime.strptime(start_date, "%d/%m/%Y")
    dt_end = datetime.strptime(end_date, "%d/%m/%Y")
    
    period = f"{dt_start.strftime('%Y%m')}-{dt_end.strftime('%Y%m')}"

    url = (
        f"https://apisidra.ibge.gov.br/values"
        f"/t/{config.get('tabela')}"
        f"/{config.get('nivel')}/{config.get('territorio')}"
        f"/v/{config.get('variaveis')}"
        f"/p/{period}"
        f"/d/s"
    )

    return url

def fetch_sinapi(config: dict, start_date: str, end_date: str, retries=3) -> list[dict]:

    url = build_sinapi_url(config=config, start_date=start_date, end_date=end_date)

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url=url, timeout=10)
            
            if response.status_code == 200:
                logging.info(f"Dados do SINAPI obtidos com sucesso na tentativa {attempt}.")
                return response.json()
            
            logging.warning(f"Tentativa {attempt}/{retries} falhou (Status: {response.status_code}). Aguardando 5s...")
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro de comunicação na tentativa {attempt}: {e}")

        time.sleep(5)

    logging.critical(f"Falha: Não foi possível obter os dados do SINAPI após {retries} tentativas.")
    response.raise_for_status()


def save_raw_sinapi(data: list[dict]):
    
    raw_dir = Path("data/bronze/ibge/sinapi")
    raw_dir.mkdir(parents=True, exist_ok=True)

    current_date = datetime.today().strftime("%Y%m%d")
    raw_path = raw_dir / f"{current_date}_response.json"

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"RAW Sinapi: {len(data)} registros salvos em {raw_path}")
    return raw_path

def extract_sinapi_data(sinapi_config: dict, start_date: str, end_date: str):
    try:
        data = fetch_sinapi(config=sinapi_config, start_date=start_date, end_date=end_date)

        if data:
            save_raw_sinapi(data=data)
        
        else:
            logging.warning(f'Nenhum dado do SINAPI encontrado!')

    except Exception as e:
        logging.error(f'Falha ao extrair dados do SINAPI: {e}')