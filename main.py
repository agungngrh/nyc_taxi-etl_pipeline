from config.config import Config
from config.logger import setup_logging, get_logger

from src.extract import Extractor
from src.transform import Transformer
from src.load import Loader

from src.data_validate import DataValidator
from src.data_reports import DataQualityReport
from utils.helpers import run_stage

setup_logging()
logger = get_logger(__name__)

def main() -> None:
    """
    Orchestrator program untuk menjalankan pipeline ETL.
    """
    try:
        config = Config()

        extractor = Extractor(config)
        transformer = Transformer(config)
        validator = DataValidator(config)
        loader = Loader(config)
        report_data = DataQualityReport(config)

        run_stage(stage_name='Extract', func=extractor.extract)
        run_stage(stage_name='Transform', func=transformer.transform)
        run_stage(stage_name='Load', func=loader.load_to_data_mart)
        run_stage(stage_name='Validator', func=validator.validate)
        run_stage(stage_name='Reporting', func=report_data.generate_report)

    except Exception as err:
        logger.error(f'Pipeline gagal dijalankan: {err}')
        raise

if __name__ == "__main__":
    main()