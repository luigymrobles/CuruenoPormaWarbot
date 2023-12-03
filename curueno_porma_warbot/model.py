from typing import TypeVar

from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base
from geoalchemy2 import Geometry


T = TypeVar("T")


def common_repr(obj: T):
    """Helper method to set the repr method for all DB Models
    Will return the class_name and the id like this:

    ```python
    Person:None
    Town:5
    Stat:40
    ```
    """
    return f"{obj.__class__.__name__}:{getattr(obj, 'id', None)}"


Base = declarative_base()
Base.id = Column(Integer, primary_key=True)
Base.__repr__ = common_repr


class Town(Base):
    __tablename__ = "town"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    coordinates = Column(Geometry('POINT'))
    alive = Column(Boolean, default=True)

    def __init__(self, name: str, coords: tuple[float, float], alive: bool = True):
        self.name = name
        self.coordinates = coords
        self.alive = alive


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    town = Column(Integer, ForeignKey("town.id"))
    picture = Column(String(1024))
    alive = Column(Boolean, default=True)

    def __init__(self, name: str, town: int | Town, picture: str, alive: bool = True):
        if isinstance(town, Town):
            town = town.tid

        self.name = name
        self.town = town
        self.picture = picture
        self.alive = alive


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    event_type = Column(String(50))
    owner = Column(Integer, ForeignKey("person.id"))

    def __init__(self, event_type: str, owner: int | Person):
        if isinstance(owner, Person):
            owner = owner.pid

        self.event_type = event_type
        self.owner = owner


class Stat(Base):
    __tablename__ = "stat"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    value = Column(String(50))
    owner = Column(Integer, ForeignKey("person.id"))

    def __init__(self, name: str, value: str, owner: int | Person):
        if isinstance(owner, Person):
            owner = owner.pid

        self.name = name
        self.value = value
        self.owner = owner


WarbotDBModel = Town | Person | Event | Stat
