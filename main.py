from config.config import Config
from config.logger import setup_logging, get_logger

from src.extract import Extractor
from src.transform import Transformer
from src.load import Loader

from src.data_validate import DataValidator
from src.data_reports import DataQualityReport

setup_logging()
logger = get_logger(__name__)


def main() -> None:
    """
    Entry point program untuk menjalankan pipeline ETL.
    """
    try:
        config = Config()

        extractor = Extractor(config)
        transformer = Transformer(config)
        validator = DataValidator(config)
        loader = Loader(config)
        report_data = DataQualityReport(config)

        extractor.extract()
        transformer.transform()
        loader.load_to_data_mart()
        validator.validate()
        report_data.generate_report()

        logger.info('Pipeline selesai')

    except Exception as err:
        logger.error(f'Pipeline gagal dijalankan: {err}')
        raise

if __name__ == "__main__":
    main()