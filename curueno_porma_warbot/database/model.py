# from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base
from typing import TypeVar


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
    __tablename__ = "Town"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    # This is disabled until we fix the column cannot be null issue
    # coordinates = Column(Geometry('POINT'), nullable=True)
    alive = Column(Boolean, default=True)

    def __init__(self, name: str, coordinates: tuple[float, float] = None, alive: bool = True):
        self.name = name
        # self.coordinates = coordinates
        self.alive = alive


class Person(Base):
    __tablename__ = "Person"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    town = Column(Integer, ForeignKey("Town.id"))
    picture = Column(String(1024), nullable=True)
    alive = Column(Boolean, default=True)

    def __init__(self, name: str, town: int | Town, picture: str = None, alive: bool = True):
        if isinstance(town, Town):
            town = town.tid

        self.name = name
        self.town = town
        self.picture = picture
        self.alive = alive


class Event(Base):
    __tablename__ = "Event"
    id = Column(Integer, primary_key=True)
    event_type = Column(String(50))
    owner = Column(Integer, ForeignKey("Person.id"))

    def __init__(self, event_type: str, owner: int | Person):
        if isinstance(owner, Person):
            owner = owner.pid

        self.event_type = event_type
        self.owner = owner


class Stat(Base):
    __tablename__ = "Stat"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    value = Column(String(50))
    owner = Column(Integer, ForeignKey("Person.id"))

    def __init__(self, name: str, value: str, owner: int | Person):
        if isinstance(owner, Person):
            owner = owner.pid

        self.name = name
        self.value = value
        self.owner = owner


WarbotDBModel = Town | Person | Event | Stat
