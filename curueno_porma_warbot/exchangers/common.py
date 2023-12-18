from abc import ABC

from curueno_porma_warbot.database.manager import DBManager


class ExchangerHandler(ABC):
    """This class defines some properties and methods available on all Handlers
    to import and export data between files and the DB.
    """
    def __init__(self, *args, **kwargs):
        self.db_manager = DBManager()
