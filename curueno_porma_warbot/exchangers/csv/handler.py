import csv
import io
from dataclasses import dataclass, asdict
from typing import Generator

from curueno_porma_warbot.exchangers.common import ExchangerHandler

# name,picture,alive,town_name,town_coords,town_alive,stat_1_name,stat_1_value,[...],event_1_type,event_1_co_owner,[...]

@dataclass
class CSVTown:
    name: str
    coords: tuple[float, float]
    alive: bool

    dict = asdict


@dataclass
class CSVStat:
    name: str
    value: str

    dict = asdict


@dataclass
class CSVPerson:
    name: str
    picture: str
    alive: bool
    town: CSVTown
    stats: list[CSVStat]

    dict = asdict


def get_row_stats(row: dict) -> list[CSVStat]:
    """Dynamically detects how many stats are there in the row
    and parses them.

    Returns a list of CSVStat objects.
    """
    stats = []
    stat_count = int(sum(1 for key in row.keys() if "stat" in key) / 2)
    for n in range(stat_count):
        stat = CSVStat(
            name=row[f"stat_{n}_name"],
            value=row[f"stat_{n}_name"],
        )
        stats.append(stat)

    return stats


class CSVHandler(ExchangerHandler):
    def __init__(self, *args, **kwargs):
        super(CSVHandler, self).__init__(*args, **kwargs)

    def import_file(self, data: io.StringIO):
        for person in self.consume(data):
            self.create_in_db(person)

    def consume(self, data: io.StringIO) -> Generator[CSVPerson, None, None]:
        people = []
        reader = csv.DictReader(data.readlines())
        for row in reader:
            person = CSVPerson(
                name=row["name"],
                picture=row["picture"],
                alive=row["alive"],
                town=CSVTown(
                    name=row["town_name"],
                    coords=row["town_coords"],
                    alive=row["town_alive"],
                ),
                stats=get_row_stats(row),
            )
            yield person

    def create_in_db(self, person: CSVPerson):
        with self.db_manager as db:
            town = db.get_or_create_town({
                "name": person.town.name,
                "alive": person.town.alive,
            })
            db_person = db.get_or_create_person({
                "name": person.name,
                "picture": person.picture,
                "alive": person.alive,
                "town": town,
            })
            for stat in person.stats:
                db.create_stat({
                    "name": stat.name,
                    "value": stat.value,
                    "owner": db_person,
                })