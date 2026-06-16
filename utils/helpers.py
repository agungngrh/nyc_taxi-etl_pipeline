import os
import pandas as pd

def ensure_file_exists(file_path: str) -> None:
    """
    memastikan file sudah ada
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f'File tidak ditemukan: {file_path}'
        )
    
def ensure_directory_exists(file_path: str) -> None:
    """
    membuat folder directory jika belum tersedia
    """
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

def read_parquet_file(file_path: str) -> pd.DataFrame:
    """
    Membaca file parquet dan mengubahnya menjadi dataframe
    """
    ensure_file_exists(file_path)
    return pd.read_parquet(file_path)

def save_to_csv(file_path: str, df: pd.DataFrame) -> None:
    """
    menyimpan dataframe ke dalam format csv
    """
    ensure_directory_exists(file_path)
    df.to_csv(file_path, index=False)

def save_to_parquet(file_path: str, df: pd.DataFrame) -> None:
    """
    menyimpan data kedalam format parquet
    """
    ensure_directory_exists(file_path)
    df.to_parquet(file_path, index=False)
    