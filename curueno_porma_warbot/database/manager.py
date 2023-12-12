from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from curueno_porma_warbot.database.model import Base, Person, Stat, Town, WarbotDBModel
from curueno_porma_warbot.utils.config import MySQLConfig
from curueno_porma_warbot.utils.error import NoDBSession
from curueno_porma_warbot.utils.log import ClassWithLogger


class DBManager(ClassWithLogger):
    """This object interacts with the DB to manage the CRUD for the models.

    Loads the configuration from the environment variables and stablishes
    connection with the MySQL database.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = MySQLConfig()

        self.session = None
        self.engine = create_engine(self.config.get_engine_uri(), echo=self.config.mysql_verbose)
        self.__get_session = sessionmaker(bind=self.engine)

        self.logger.info("Ready!")

    def setup(self) -> None:
        """Creates all tables in the DB from the DB models."""
        Base.metadata.create_all(bind=self.engine)

    def __check_session(self):
        """Raises NoDBSession exception if session does not exist."""
        if self.session is None:
            raise NoDBSession("DB Session does not exist.")

    def __enter__(self) -> "DBManager":
        """Creates a new session."""
        self.session = self.__get_session()
        self.logger.info("New DB session created")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits the changes from the session to the DB and
        destroys the current session.

        :raises NoDBSession: if session does not exist.
        """
        self.__check_session()
        self.session.commit()
        self.logger.info("Changes commited")
        self.session = None
        self.logger.info("DB Session closed")

    def __create_and_add(self, db_model: WarbotDBModel, data: dict) -> WarbotDBModel:
        """Creates a new object from the provided data and adds
        it to the session.

        :param db_model: The DB model to use.
        :param data: The parameters used for the new object.
        :raises NoDBSession: if session does not exist.
        :returns: db_model instance with said values
        """
        self.__check_session()
        obj = db_model(**data)
        self.session.add(obj)
        return obj

    def __get_some_or_all_by_id(self, db_model: WarbotDBModel, _id: int | None = None) -> Generator[WarbotDBModel, None, None]:
        """Fetches 1, many or all objects for the db_model and _id provided.

        :param db_model: The db_model we are searching for.
        :param _id: The _id we are searching for. If no _id provided, will return all from DB.
        :returns: A generator with the documents from DB response.
        """
        self.__check_session()
        if _id is not None:
            yield from self.session.query(db_model).filter(db_model.id == _id)
        else:
            for person in self.session.query(db_model).all():
                yield person

    def create_person(self, person_data: dict) -> Person:
        """Creates the Person object and adds it to the session

        :returns: The new Person object.
        """
        return self.__create_and_add(Person, person_data)

    def get_person(self, _id: int | None = None) -> Generator[Person, None, None]:
        """Fetches the Person from database with id _id.
        Will return all Person objects in DB if _id is None.
        """
        return self.__get_some_or_all_by_id(Person, _id)

    def create_stat(self, stat_data: dict) -> Stat:
        """Creates the Stat object and adds it to the session

        :returns: The new Stat object.
        """
        return self.__create_and_add(Stat, stat_data)

    def get_stat(self, _id: int | None = None) -> Generator[Stat, None, None]:
        """Fetches the Stat from database with id _id.
        Will return all Stat objects in DB if _id is None.
        """
        return self.__get_some_or_all_by_id(Stat, _id)

    def create_town(self, town_data: dict) -> Town:
        """Creates the Town object and adds it to the session

        :returns: The new Town object.
        """
        return self.__create_and_add(Town, town_data)

    def get_town(self, _id: int | None = None) -> Generator[Town, None, None]:
        """Fetches the Town from database with id _id.
        Will return all Town objects in DB if _id is None.
        """
        return self.__get_some_or_all_by_id(Town, _id)
