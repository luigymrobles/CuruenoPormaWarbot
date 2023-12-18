"""All these models are used by FastAPI to be able to serve DB models"""
from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        from_attributes = True

class Town(BaseModelORM):
    id: int
    name: str
    # coordinates: tuple[float, float] | None = None
    alive: bool


class Person(BaseModelORM):
    id: int
    name: str
    town: int
    picture: str | None = None
    alive: bool


class Event(BaseModelORM):
    id: int
    event_type: str
    owner_1: int
    owner_2: int


class Stat(BaseModelORM):
    id: int
    name: str
    value: str
    owner: int

WarbotDBModel = Town | Person | Event | Stat
