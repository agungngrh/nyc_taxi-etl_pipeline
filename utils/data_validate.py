import pandas as pd
from config.config import Config
from config.logger import get_logger
from utils.helpers import (
    read_parquet_file,
    save_to_csv,
)

logger = get_logger(__name__)


class DataValidator:
    """
    Bertanggung jawab untuk memisahkan data valid dan invalid.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def _validate_duration(self, df: pd.DataFrame) -> pd.Series:
        """
        Menghasilkan mask data dengan durasi perjalanan tidak valid.
        """
        return df['tpep_pickup_datetime'] >= df['tpep_dropoff_datetime']

    def _validate_distance(self, df: pd.DataFrame) -> pd.Series:
        """
        Menghasilkan mask data dengan jarak perjalanan tidak valid.
        """
        return df['trip_distance'] <= 0

    def _read_data(self) -> pd.DataFrame:
        """
        Membaca data hasil transformasi dari file parquet.
        """
        return read_parquet_file(self.config.TRANSFORMED_FILE)

    def _build_invalid_dataframe(self, df: pd.DataFrame, duration_mask: pd.Series, distance_mask: pd.Series, invalid_mask: pd.Series) -> pd.DataFrame:
        """
        Membuat dataframe karantina beserta detail jenis error.
        """
        invalid_df = df.loc[invalid_mask].copy()

        invalid_df['duration_invalid'] = duration_mask.loc[invalid_mask]
        invalid_df['distance_invalid'] = distance_mask.loc[invalid_mask]

        invalid_df['error_type'] = ''

        invalid_df.loc[
            invalid_df['duration_invalid'],
            'error_type'
        ] += 'duration invalid'

        invalid_df.loc[
            invalid_df['distance_invalid'],
            'error_type'
        ] += '; distance invalid'

        invalid_df['error_type'] = (
            invalid_df['error_type']
            .str.lstrip('; ')
        )

        return invalid_df

    def _save_results(self, valid_df: pd.DataFrame, invalid_df: pd.DataFrame) -> None:
        """
        Menyimpan data valid dan invalid ke folder mart_cleaned.
        """
        save_to_csv(self.config.VALID_FILE, valid_df)
        logger.info(f'Data valid disimpan di: {self.config.VALID_FILE}')

        save_to_csv(self.config.INVALID_FILE, invalid_df)
        logger.info(f'Data invalid disimpan di: {self.config.INVALID_FILE}')

    def validate(self) -> None:
        """
        Menjalankan proses validasi data quality.
        Data invalid dipisahkan ke file karantina.
        """
        logger.info('Mulai menjalankan proses validasi data')

        try:
            df = self._read_data()

            duration_mask = self._validate_duration(df)
            distance_mask = self._validate_distance(df)

            invalid_mask = duration_mask | distance_mask

            invalid_df = self._build_invalid_dataframe(
                df=df,
                duration_mask=duration_mask,
                distance_mask=distance_mask,
                invalid_mask=invalid_mask,
            )

            valid_df = df.loc[~invalid_mask].copy()

            self._save_results(
                valid_df=valid_df,
                invalid_df=invalid_df,
            )

            logger.info('Proses validasi data selesai')

        except Exception as err:
            logger.error(f'Terjadi error saat proses validasi data: {err}')
            raise