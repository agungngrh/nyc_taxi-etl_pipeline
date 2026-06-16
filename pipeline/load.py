from config.config import Config
from config.logger import get_logger
from utils.helpers import (
    read_parquet_file,
    save_to_csv,
)

logger = get_logger(__name__)

class Loader:
    """
    Bertanggung jawab untuk memuat data hasil transformasi
    ke dalam data mart.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        
    def load_to_data_mart(self) -> None:
        """
        Membaca data hasil transformasi kemudian
        menyimpannya ke data mart.
        """
        logger.info('Memulai proses load data')

        try:
            df = read_parquet_file(self.config.TRANSFORMED_FILE)
            save_to_csv(file_path=self.config.MART_FILE, df=df)

            logger.info('Proses load data selesai')

        except FileNotFoundError as err:
            logger.error(f'File tidak ditemukan: {str(err)}')
            raise
        except Exception as err:
            logger.error(f'Gagal menjalankan proses load data: {err}')
            raise