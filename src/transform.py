import re
import pandas as pd
from config.config import Config
from config.logger import get_logger
from utils.helpers import read_csv_file, read_parquet_file, save_to_parquet

logger = get_logger(__name__)


PAYMENT_MAPPING = {
    0: 'Unknown',
    1: 'Credit Card',
    2: 'Cash',
    3: 'No Charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided Trip',
}

FLAG_MAP = {
    'Y': 'Store and Forward',
    'N': 'Normal',
}


class Transformer:
    """
    bertanggung jawab untuk mentransformasi data mentah menjadi data yg bervariatif
    dan mudah untuk dianalisis
    """
    def __init__(self, config: Config) -> None:
        self.config = config

    def _column_to_snake_case(self, name: str) -> str:
        """
        helper function untuk mengubah nama kolom menjadi format snake_case
        """
        column = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
        column = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', column)
        return column.lower()
    
    def _rename_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        mengubah nama kolom menjadi format snake_case
        """
        df.columns = [self._column_to_snake_case(col) for col in df.columns]
        return df
    
    def _add_trip_duration(self, df: pd.DataFrame) -> pd.DataFrame:
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')

        df['trip_duration_minutes'] = (
            df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
        ).dt.total_seconds() / 60
        return df
    
    def _add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df['pickup_date'] = df['tpep_pickup_datetime'].dt.date
        df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
        df['pickup_day_name'] = df['tpep_pickup_datetime'].dt.day_name()
        df['is_weekend'] = df['tpep_pickup_datetime'].dt.day_of_week.isin([5, 6])
        return df
    
    def _add_time_period(self, df: pd.DataFrame) -> pd.DataFrame:
        df['time_period'] = pd.cut(
            df['pickup_hour'],
            bins=[0, 6, 11, 16, 20, 24],
            labels=['Late Night', 'Morning', 'Afternoon', 'Evening Rush', 'Night'],
            right=False,
            include_lowest=True
        )
        return df
    
    def _mapping_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        df['payment_type'] = df['payment_type'].map(PAYMENT_MAPPING).fillna('Unknown')
        df['store_and_fwd_flag'] = df['store_and_fwd_flag'].map(FLAG_MAP).fillna('Unknown')
        return df
    
    def _feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        membuat fitur/kolom baru untuk menambah variasi data dan kebutuhan analisis
        """
        df = self._add_trip_duration(df)
        df = self._add_time_features(df)
        df = self._add_time_period(df)
        df = self._mapping_categorical(df)
        return df
    
    def _join_location(self, df: pd.DataFrame, zone_df: pd.DataFrame, location_col: str, prefix: str) -> pd.DataFrame:
        """
        """
        lookup_df = zone_df[['locationid', 'borough', 'zone']].copy()
        mapped_df = df.merge(
            lookup_df,
            left_on=location_col,
            right_on='locationid',
            how='left'
        )
        mapped_df = mapped_df.rename(
            columns={
                'borough': f'{prefix}_borough',
                'zone': f'{prefix}_zone'
            }
        )
        if 'locationid' in mapped_df.columns:
            mapped_df = mapped_df.drop(columns='locationid')

        return mapped_df
    
    def _mapping_location(self, df: pd.DataFrame, zone_df: pd.DataFrame) -> pd.DataFrame:
        """
        """
        zone_df = zone_df.copy()
        zone_df.columns = zone_df.columns.str.lower()

        df = self._join_location(df, zone_df, 'pu_location_id', 'pickup')
        df = self._join_location(df, zone_df, 'do_location_id', 'dropoff')
        return df
    
    def transform(self) -> None:
        """
        menjalankan proses seluruh transofrmasi data
        """
        logger.info('Mulai menjalankan proses transformasi data')

        try:
            df = read_parquet_file(self.config.TAXI_FILE)
            zone_df = read_csv_file(self.config.ZONE_FILE)

            df = self._rename_column(df)
            df = self._feature_engineering(df)
            df = self._mapping_location(df, zone_df)

            save_to_parquet(file_path=self.config.TRANSFORMED_FILE, df=df)

            logger.info(f'Data hasil transformasi disimpan di: {self.config.TRANSFORMED_FILE}')
            logger.info('Proses transformasi data selesai')

        except Exception as err:
            logger.error(f'Terjadi error saat proses transformasi: {str(err)}')
            raise