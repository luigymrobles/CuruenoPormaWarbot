from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from curueno_porma_warbot.model import Base, Person, Stat, Town, WarbotDBModel
from curueno_porma_warbot.utils.config import MySQLConfig
from curueno_porma_warbot.utils.log import ClassWithLogger


class DBManager(ClassWithLogger):
    def __init__(self, *args, **kwargs):
        load_dotenv()
        super(DBManager).__init__(*args, **kwargs)
        self.config = MySQLConfig()

    def __enter__(self) -> "DBManager":
        self.logger.info("Enter DBManager")
        engine = create_engine(self.config.get_engine_uri(), echo=True)

        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.logger.info("DB Session init OK")
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()
        self.logger.info("Changes commited to DB OK")

    def __create_and_add(self, db_model: WarbotDBModel, data: dict):
        obj = db_model(**data)
        self.session.add(obj)
        return obj

    def create_person(self, person_data: dict) -> Person:
        return self.__create_and_add(Person, person_data)

    def create_stat(self, stat_data: dict) -> Stat:
        return self.__create_and_add(Stat, stat_data)

    def create_town(self, town_data: dict) -> Town:
        return self.__create_and_add(Town, town_data)
