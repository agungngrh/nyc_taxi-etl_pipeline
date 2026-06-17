import logging
import os
from config.config import Config

_is_configured = False

def setup_logging() -> None:
    '''
    Konfigurasi logging utama
    '''
    if logging.getLogger().hasHandlers():
        return
    
    global _is_configured
    if _is_configured:
        return
    
    os.makedirs(Config.LOGS_DIR, exist_ok=True)

    file_name = os.path.join(
        Config.LOGS_DIR,"pipeline.log")

    # Setup logging root
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)5s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', 
        handlers=[
            logging.StreamHandler(), # Menampilkan di terminal
            logging.FileHandler(file_name, mode='a', encoding='utf-8')  # Menyimpan ke file 
        ]
    )
    
    _is_configured = True


def get_logger(name: str) -> logging.Logger:
    '''
    Dipanggil untuk setiap module untuk mendapatkan logger
    '''
    setup_logging()
    return logging.getLogger(name)