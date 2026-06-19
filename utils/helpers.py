import os
import pandas as pd
import time
from typing import Callable
from config.logger import get_logger

logger = get_logger(__name__)

def ensure_file_exists(file_path: str) -> None:
    """
    Helper function untuk memastikan file sudah ada
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f'File tidak ditemukan: {file_path}'
        )

def create_directory(directory: str) -> None:
    """
    Helper function untuk membuat directory jika belum tersedia.
    """
    os.makedirs(directory, exist_ok=True)

def ensure_parent_directory(file_path: str) -> None:
    """
    Helper function untuk membuat folder directory jika belum tersedia
    """
    directory = os.path.dirname(file_path)
    if directory:
        create_directory(directory)

def read_parquet_file(file_path: str) -> pd.DataFrame:
    """
    Helper function untuk membaca file parquet dan mengubahnya menjadi dataframe
    """
    ensure_file_exists(file_path)
    return pd.read_parquet(file_path)

def read_csv_file(file_path: str, low_memory: bool= False) -> pd.DataFrame:
    """
    Helper function untuk membaca file format csv
    """
    ensure_file_exists(file_path)
    return pd.read_csv(file_path, low_memory=low_memory)

def save_to_csv(file_path: str, df: pd.DataFrame) -> None:
    """
    Helper function untuk menyimpan dataframe ke dalam format csv
    """
    ensure_parent_directory(file_path)
    df.to_csv(file_path, index=False)

def save_to_parquet(file_path: str, df: pd.DataFrame) -> None:
    """
    Helper function untuk menyimpan data kedalam format parquet
    """
    ensure_parent_directory(file_path)
    df.to_parquet(file_path, index=False)
    
def run_stage(stage_name: str, func: Callable) -> None:
    """
    Menjalankan sebuah stage pipeline dan mencatat waktu eksekusinya
    """
    start_time = time.time()
    func()
    duration = time.time() - start_time

    logger.info(
        f'Stage {stage_name} selesai dalam {duration:.2f} detik'
    )