import logging

from curueno_porma_warbot.utils.log import setup_logging
from curueno_porma_warbot.warbot import CuruenoPormaWarbot


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger()

    with CuruenoPormaWarbot() as warbot:
        pass

    logger.info("End")
