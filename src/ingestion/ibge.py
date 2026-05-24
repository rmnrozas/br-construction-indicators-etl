from datetime import datetime
from pathlib import Path

import requests
import json
import time
import logging

class SINAPIIngestor():
    def __init__(self, start_date: str, end_date: str, retries: int = 3):

        self.start_date = start_date
        self.end_date = end_date
        self.retries = retries
        self.base_url = 'https://apisidra.ibge.gov.br/values'

        # Conversão de datas para o formato necessário da URL
        dt_start = datetime.strptime(self.start_date, "%d/%m/%Y")
        dt_end = datetime.strptime(self.end_date, "%d/%m/%Y")
        self.period = f"{dt_start.strftime('%Y%m')}-{dt_end.strftime('%Y%m')}"

    def _build_url(self, config: dict):
        
        url = (
            f"{self.base_url}"
            f"/t/{config.get('tabela')}"
            f"/{config.get('nivel')}/{config.get('territorio')}"
            f"/v/{config.get('variaveis')}"
            f"/p/{self.period}"
            f"/d/s"
        )

        return url

    def _fetch_sinapi(self, config: dict):

        url = self._build_url(config=config)

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(url=url, timeout=10)
                
                if response.status_code == 200:
                    logging.info(f"Dados do SINAPI obtidos com sucesso na tentativa {attempt}.")
                    return response.json()
                
                logging.warning(f"Tentativa {attempt}/{self.retries} falhou (Status: {response.status_code}). Aguardando 5s...")
                
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro de comunicação na tentativa {attempt}: {e}")

            time.sleep(5)

        logging.critical(f"Falha: Não foi possível obter os dados do SINAPI após {self.retries} tentativas.")
        response.raise_for_status()


    def _save_sinapi(self, data: list[dict]):
        
        raw_dir = Path("data/bronze/ibge/sinapi")
        raw_dir.mkdir(parents=True, exist_ok=True)

        current_date = datetime.today().strftime("%Y%m%d")
        raw_path = raw_dir / f"{current_date}_response.json"

        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logging.info(f"RAW Sinapi: {len(data)} registros salvos em {raw_path}")
        return raw_path

    def extract_sinapi(self, sinapi_config: dict):
        try:
            data = self._fetch_sinapi(config=sinapi_config)

            if data:
                self._save_sinapi(data=data)
            
            else:
                logging.warning(f'Nenhum dado do SINAPI encontrado!')

        except Exception as e:
            logging.error(f'Falha ao extrair dados do SINAPI: {e}')