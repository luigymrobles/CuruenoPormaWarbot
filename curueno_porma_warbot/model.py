from typing import TypeVar

from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from geoalchemy2 import Geometry

from curueno_porma_warbot.utils.config import MySQLConfig


T = TypeVar("T")


def common_repr(obj: T):
    return f"{obj.__class__.__name__}:{getattr(obj, 'id', None)}"


Base = declarative_base()
Base.id = Column(Integer, primary_key=True)
Base.__repr__ = common_repr


class Person(Base):
    __tablename__ = "person"
    name = Column(String(120))
    picture = Column(String(1024))
    # stats = Column(ForeignKey("stat.id"))
    alive = Column(Boolean, default=True)

    def __init__(self, uid: int, name: str, picture: str, stats: str, alive: bool = True):
        self.id = uid
        self.name = name
        self.picture = picture
    #    self.stats = stats
        self.alive = alive


class Stat(Base):
    __tablename__ = "stat"


class Town(Base):
    __tablename__ = "town"
    coordinates = Column(Geometry('POINT'))
    alive = Column(Boolean, default=True)


WarbotDBModel = Person | Stat | Town