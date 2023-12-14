from dotenv import load_dotenv

from curueno_porma_warbot.database.manager import DBManager
from curueno_porma_warbot.twitter_api.client import TwitterAPIClient
from curueno_porma_warbot.utils.log import ClassWithLogger, setup_logging


class CuruenoPormaWarbot(ClassWithLogger):
    """Main class for the project. Holds all the logic for the Warbot."""
    def __init__(self, *args, **kwargs):
        setup_logging()
        load_dotenv()
        super().__init__(*args, **kwargs)
        self.tw_client = TwitterAPIClient()
        self.db_manager = DBManager()
