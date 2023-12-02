from dataclasses import dataclass, field


@dataclass
class Event:
    pass


@dataclass
class EventList:
    pass


@dataclass
class Town:
    name: str
    coords: tuple[int, int]
    alive: bool = True


@dataclass
class Person:
    id: str
    name: str
    picture: str
    stats: list = field(default_factory=list)
    alive: bool = True
