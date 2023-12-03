from typing import Optional, Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from curueno_porma_warbot.model import Base, Person, Stat, Town, WarbotDBModel
from curueno_porma_warbot.utils.config import MySQLConfig
from curueno_porma_warbot.utils.error import NoDBSession
from curueno_porma_warbot.utils.log import ClassWithLogger


class DBManager(ClassWithLogger):
    def __init__(self, *args, **kwargs):
        load_dotenv()
        super().__init__(*args, **kwargs)
        self.config = MySQLConfig()

        self.session = None
        self.engine = create_engine(self.config.get_engine_uri(), echo=self.config.mysql_verbose)
        self.__get_session = sessionmaker(bind=self.engine)

        self.logger.info("Ready!")

    def setup(self):
        Base.metadata.create_all(bind=self.engine)

    def __check_session(self):
        if self.session is None:
            raise NoDBSession("DB Session does not exist.")

    def __enter__(self) -> "DBManager":
        self.session = self.__get_session()
        self.logger.info("New DB session created")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__check_session()
        self.session.commit()
        self.logger.info("Changes commited")
        self.session = None
        self.logger.info("DB Session closed")

    def __create_and_add(self, db_model: WarbotDBModel, data: dict) -> WarbotDBModel:
        self.__check_session()
        obj = db_model(**data)
        self.session.add(obj)
        return obj

    def __get_some_or_all_by_id(self, db_model: WarbotDBModel, _id: int | None = None) -> Generator[WarbotDBModel, None, None]:
        self.__check_session()
        if _id is not None:
            yield from self.session.query(db_model).filter(db_model.id == _id)
        else:
            for person in self.session.query(db_model).all():
                yield person

    def create_person(self, person_data: dict) -> Person:
        return self.__create_and_add(Person, person_data)

    def get_person(self, _id: int | None = None) -> Generator[Person, None, None]:
        return self.__get_some_or_all_by_id(Person, _id)

    def create_stat(self, stat_data: dict) -> Stat:
        return self.__create_and_add(Stat, stat_data)

    def get_stat(self, _id: int | None = None) -> Generator[Stat, None, None]:
        return self.__get_some_or_all_by_id(Stat, _id)

    def create_town(self, town_data: dict) -> Town:
        return self.__create_and_add(Town, town_data)

    def get_town(self, _id: int | None = None) -> Generator[Town, None, None]:
        return self.__get_some_or_all_by_id(Town, _id)
