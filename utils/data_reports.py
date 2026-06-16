import os
import pandas as pd
from typing import Literal
from config.config import Config
from config.logger import get_logger

logger = get_logger(__name__)


class DataQualityReport:
    """
    Bertanggung jawab untuk membuat format laporan analisis sederhana kualitas data
    """
    def __init__(self, config: Config) -> None:
        self.config = config

    def _load(self, path: str, fmt: Literal['parquet', 'csv']) -> pd.DataFrame:
        """
        Membaca file parquet atau csv dari path yang diberikan.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f'File tidak ditemukan: {path}')
        return pd.read_parquet(path) if fmt == 'parquet' else pd.read_csv(path, low_memory=False)

    def _pct(self, n: int, total: int) -> float:
        """
        Menghitung persentase n terhadap total.
        """
        return (n / total * 100) if total > 0 else 0.0

    def _write_summary(self, f, df: pd.DataFrame, valid_df: pd.DataFrame, invalid_df: pd.DataFrame) -> None:
        total = len(valid_df) + len(invalid_df)
        f.write('- DATA QUALITY REPORT\n\n')
        f.write(f'Total Rows : {len(df)}\n')
        f.write(f'Total Columns : {len(df.columns)}\n')
        f.write(f'Duplicate Rows : {df.duplicated().sum()}\n')
        f.write(f'Valid Records : {len(valid_df)} ({self._pct(len(valid_df), total):.2f}%)\n')
        f.write(f'Invalid Records: {len(invalid_df)} ({self._pct(len(invalid_df), total):.2f}%)\n\n')

    def _write_missing_values(self, f, df: pd.DataFrame) -> None:
        f.write('- MISSING VALUES SUMMARY\n\n')
        null_summary = df.isnull().sum()
        null_summary = null_summary[null_summary > 0].sort_values(ascending=False)
        if null_summary.empty:
            f.write('Tidak ditemukan missing values\n')
        else:
            for col, val in null_summary.items():
                f.write(f'{col}: {val}\n')
        f.write('\n')

    def _write_invalid_summary(self, f, invalid_df: pd.DataFrame) -> None:
        f.write('- INVALID DATA SUMMARY\n\n')
        if invalid_df.empty:
            f.write('Tidak ditemukan data invalid\n')
        elif 'error_type' not in invalid_df.columns:
            logger.warning("Kolom 'error_type' tidak ditemukan di invalid_df")
            f.write(f"Total invalid records: {len(invalid_df)} (kolom 'error_type' tidak tersedia)\n")
        else:
            for error, count in invalid_df['error_type'].value_counts().items():
                f.write(f'{error}: {count}\n')

    def generate(self) -> str:
        """
        Menghasilkan report kualitas data dalam format txt.
        """
        logger.info('Memulai pembuatan data quality report')
        try:
            df = self._load(self.config.TRANSFORMED_FILE, 'parquet')
            valid_df = self._load(self.config.VALID_FILE, 'csv')
            invalid_df = self._load(self.config.INVALID_FILE, 'csv')

            os.makedirs(self.config.REPORTS_DIR, exist_ok=True)
            report_file = os.path.join(self.config.REPORTS_DIR, 'data_quality_report.txt')

            with open(report_file, 'w', encoding='utf-8') as f:
                self._write_summary(f, df, valid_df, invalid_df)
                self._write_missing_values(f, df)
                self._write_invalid_summary(f, invalid_df)

            logger.info(
                f'Report berhasil dibuat: {report_file} — '
                f'total: {len(df)}, valid: {len(valid_df)}, invalid: {len(invalid_df)}'
            )
            return report_file

        except FileNotFoundError as err:
            logger.error(f'File sumber tidak ditemukan: {err}')
            raise
        except Exception as err:
            logger.error(f'Gagal membuat report: {err}')
            raise