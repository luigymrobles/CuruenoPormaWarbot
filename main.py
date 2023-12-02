import logging

from src.utils.log import setup_logging
from src.warbot import CuruenoPormaWarbot


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger()

    with CuruenoPormaWarbot() as warbot:
        pass

    logger.info("End")
