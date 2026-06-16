import os

class Config:
    """
    Konfigurasi folder, file path dan url
    """
    TAXI_URL = os.getenv(
        'DATA_URL',
        f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet'
    )
    
    ZONE_URL = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'

    # base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # folder path
    RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
    TRANSFORMED_DIR = os.path.join(BASE_DIR, 'data', 'transformed')
    MART_DIR = os.path.join(BASE_DIR, 'data', 'mart')
    MART_CLEANED_DIR = os.path.join(BASE_DIR, 'data', 'mart_cleaned')
    REPORTS_DIR = os.path.join(BASE_DIR, 'data', 'reports')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')

    # file path
    TAXI_FILE = os.path.join(RAW_DIR, 'yellow_tripdata_2026-01.parquet')
    ZONE_FILE = os.path.join(RAW_DIR, 'taxi_zone_lookup.csv')
    TRANSFORMED_FILE = os.path.join(TRANSFORMED_DIR, 'taxi_transformed.parquet')
    MART_FILE = os.path.join(MART_DIR, 'taxi_mart.csv')
    VALID_FILE = os.path.join(MART_CLEANED_DIR, 'valid_data.csv')
    INVALID_FILE = os.path.join(MART_CLEANED_DIR, 'invalid_data.csv')
    LOGS_FILE = os.path.join(LOGS_DIR, 'pipeline.log')
