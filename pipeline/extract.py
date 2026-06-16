import os
import requests
from requests.exceptions import HTTPError, RequestException
from config.config import Config
from config.logger import get_logger
from utils.helpers import ensure_directory_exists

logger = get_logger(__name__)

class Extractor:
    """
    Proses download data mentah dari sumber eksternal
    """
    def __init__(self, config: Config) -> None:
        self.config = config

    
    def _download_file(self, url: str, file_path: str, timeout: int=10, chunk_size: int=1024 * 1024 * 8) -> None:
        """
        Download file data URL dan menyimpanya ke local storage
        """
        if os.path.exists(file_path):
            logger.info(
                f'File sudah tersedia. Dowload dilewati: {file_path}'
            )
            return
        
        ensure_directory_exists(file_path)

        logger.info(f'Mulai mendowload data url: {url}')

        try:
            with requests.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()

                with open(file_path, 'wb') as output_file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            output_file.write(chunk)

            logger.info(f'Download selesai: {file_path}')

        except HTTPError as http_err:
            logger.error(f'HTTP error: {str(http_err)}')
            raise
        except RequestException as req_err:
            logger.error(f'Request error: {str(req_err)}')
            raise
        except Exception as err:
            logger.error(f'Terjadi error lainnya: {str(err)}')
            raise
        

    def extract(self) -> None:
        """
        Menjalankan proses ekstraksi data
        """
        logger.info('Mulai menjalankan proses ektraksi data')

        self._download_file(url=self.config.TAXI_URL, file_path=self.config.TAXI_FILE)
        self._download_file(url=self.config.ZONE_URL, file_path=self.config.ZONE_FILE)

        logger.info("Proses ekstraksi data selesai")
        


