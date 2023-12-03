import logging
from colorlog import ColoredFormatter


def setup_logging(level: int = logging.DEBUG):
    """Configures the logging for the project.

    Default level is DEBUG, but can be changed if passed as an argument.

    All handlers display colored log messages with format:
    `{level} {datetime} {message}`

    Adds the following handlers:
    - Console handler
    """
    # We can append new handlers in the future, for Telegram, Discord for ex.
    handlers = []

    log_formatter = ColoredFormatter(
        "%(log_color)s%(name)-12s%(reset)s %(log_color)s%(levelname)-8s%(reset)s %(blue)s%(asctime)s%(reset)s %(white)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    handlers.append(console_handler)

    logging.basicConfig(
        level=level,
        handlers=handlers,
    )


class ClassWithLogger:
    """This class provides a default logger attribute to any class that inherits from it."""
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
