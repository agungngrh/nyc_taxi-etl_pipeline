from config.config import Config
from config.logger import setup_logging, get_logger

from pipeline.extract import Extractor
from pipeline.transform import Transformer
from pipeline.load import Loader

from utils.data_validate import DataValidator
from utils.data_reports import DataQualityReport

setup_logging()
logger = get_logger(__name__)


def main() -> None:
    """
    Entry point program untuk menjalankan pipeline ETL.
    """
    try:
        logger.info('Mulai menjalankan Pipeline')

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