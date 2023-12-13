from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_utils.functions import drop_database

from curueno_porma_warbot.database.model import Base, Person, Stat, Town, WarbotDBModel, Event
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

    def setup(self) -> None:
        """Creates all tables in the DB from the DB models."""
        self.logger.info("Setting up DB...")

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Base.metadata.create_all(bind=self.engine)
        self.logger.info("Setting up DB...OK")

    def delete_all_tables(self) -> None:
        if database_exists(self.engine.url):
            drop_database(self.engine.url)

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

    @staticmethod
    def _clean_none(filter_dict: dict) -> dict:
        """Helper method to clean all undefined fields"""
        keys_to_delete = [
            key
            for key, value
            in filter_dict.items()
            if value is None
        ]
        for key in keys_to_delete:
            del filter_dict[key]

        return filter_dict

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

    def query_object(self, obj: WarbotDBModel, filter_dict: dict) -> list[WarbotDBModel]:
        filter_dict = self._clean_none(filter_dict)
        return self.session.query(obj).filter_by(**filter_dict)

    def query_town(
        self,
        id: int | None = None,
        name: str | None = None,
        alive: bool | None = None
    ) -> list[Town]:
        filter_dict = {
            "id": id,
            "name": name,
            "alive": alive,
        }
        return self.query_object(Town, filter_dict)

    def query_person(
        self,
        id: int | None = None,
        name: str | None = None,
        town: int | None = None,
        alive: bool | None = None
    ) -> list[Person]:
        filter_dict = {
            "id": id,
            "name": name,
            "town": town,
            "alive": alive,
        }
        return self.query_object(Person, filter_dict)

    def query_event(
            self,
            id: int | None = None,
            event_type: str | None = None,
            owner: int | None = None
    ) -> list[Event]:
        filter_dict = {
            "id": id,
            "event_type": event_type,
            "owner": owner,
        }
        return self.query_object(Event, filter_dict)

    def query_stat(
            self,
            id: int | None = None,
            name: str | None = None,
            value: str | None = None,
            owner: int | None = None
    ) -> list[Stat]:
        filter_dict = {
            "id": id,
            "name": name,
            "value": value,
            "owner": owner,
        }
        return self.query_object(Stat, filter_dict)

    def create_town(self, town_data: dict) -> Town:
        """Creates the Town object and adds it to the session

        :returns: The new Town object.
        """
        return self.__create_and_add(Town, town_data)

    def create_person(self, person_data: dict) -> Person:
        """Creates the Person object and adds it to the session

        :returns: The new Person object.
        """
        return self.__create_and_add(Person, person_data)

    def create_event(self, event_data: dict) -> Event:
        """Creates the Stat object and adds it to the session

        :returns: The new Stat object.
        """
        return self.__create_and_add(Event, event_data)

    def create_stat(self, stat_data: dict) -> Stat:
        """Creates the Stat object and adds it to the session

        :returns: The new Stat object.
        """
        return self.__create_and_add(Stat, stat_data)
