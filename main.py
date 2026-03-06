from src.vector_editor.config.config import get_config
from src.vector_editor.logger.manager import get_logger, setup_logging


def main():
    pass


if __name__ == "__main__":
    config = get_config()
    setup_logging(config.logger_adapter)
    logger = get_logger(__name__)
    logger.info("Program starts")

    main()
