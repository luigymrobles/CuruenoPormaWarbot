from fastapi import FastAPI

from curueno_porma_warbot.database.schema import Town, Person, Event, Stat
from curueno_porma_warbot.warbot import CuruenoPormaWarbot

app = FastAPI()
warbot = CuruenoPormaWarbot()

DUMMY_DATA = {
    "town": [
        {
            "name": "Curueño",
        },
        {
            "name": "Valladolid",
        },
        {
            "name": "Madrid",
        },
        {
            "name": "Zaragoza",
        },
    ],
    "person": [
        {
            "name": "Luis",
            "town": 1,
        },
        {
            "name": "Jorge",
            "town": 3,
        },
        {
            "name": "Nacho",
            "town": 2,
        },
    ],
}


@app.get("/")
def index() -> str:
    """Endpoint to redirect to docs"""
    return "Go to /docs"


@app.get("/setup")
def init_db() -> str:
    """Initializes the DB and creates the tables."""
    with warbot.db_manager as db:
        db.setup()
    return "ok"

@app.delete("/setup")
def delete_db() -> str:
    """Deletes the whole DB."""
    with warbot.db_manager as db:
        db.delete_all_tables()
    return "ok"

@app.get("/dummy")
def dummy_data() -> str:
    """Fills the DB with some dummy data."""
    with warbot.db_manager as db:
        for town_data in DUMMY_DATA["town"]:
            _ = db.create_town(town_data)

    with warbot.db_manager as db:
        for person_data in DUMMY_DATA["person"]:
            _ = db.create_person(person_data)
    return "ok"

@app.get("/town/{town_id}")
def query_town_by_id(town_id) -> list[Town]:
    """Queries a town by its id."""
    with warbot.db_manager as db:
        towns = db.query_town(id=town_id)
    return towns


@app.get("/town/")
def query_town_by_params(
    name: str | None = None,
    alive: bool | None = None
) -> list[Town]:
    """Queries a town by its parameters."""
    with warbot.db_manager as db:
        towns = db.query_town(
            name=name,
            alive=alive,
        )
    return towns

@app.get("/person/{person_id}")
def query_person_by_id(person_id: int) -> list[Person]:
    """Queries a person by its id."""
    with warbot.db_manager as db:
        person = db.query_person(id=person_id)
    return person


@app.get("/person/")
def query_person_by_params(
    name: str | None = None,
    town: int | None = None,
    alive: bool | None = None
) -> list[Person]:
    """Queries a person by its parameters."""
    with warbot.db_manager as db:
        people = db.query_person(
            name=name,
            town=town,
            alive=alive,
        )
    return people


@app.get("/event/{event_id}")
def query_event_by_id(event_id) -> list[Event]:
    """Queries an event by its id."""
    with warbot.db_manager as db:
        events = db.query_event(id=event_id)
    return events


@app.get("/event/")
def query_event_by_params(
    event_type: str | None = None,
    owner: int | None = None
) -> list[Event]:
    """Queries an event by its parameters."""
    with warbot.db_manager as db:
        events = db.query_event(
            event_type=event_type,
            owner=owner,
        )
    return events


@app.get("/stat/{stat_id}")
def query_stat_by_id(stat_id) -> list[Stat]:
    """Queries a stat by its id."""
    with warbot.db_manager as db:
        stats = db.query_stat(id=stat_id)
    return stats


@app.get("/stat/")
def query_stat_by_params(
    name: str | None = None,
    value: str | None = None,
    owner: int | None = None
) -> list[Stat]:
    """Queries a stat by its parameters."""
    with warbot.db_manager as db:
        stats = db.query_stat(
            name=name,
            value=value,
            owner=owner,
        )
    return stats
