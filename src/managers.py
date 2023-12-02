import csv
import io

from src.model import Person
from src.utils.error import PersonNotFound
from src.utils.log import ClassWithLogger


class PersonManager(ClassWithLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.people = set()

    def load_from_csv(self, data: io.StringIO) -> int:
        reader = csv.DictReader(f=data.read())

        p_count = 0
        for p_count, person in enumerate(reader, 1):
            self.people.add(Person(**person))

        self.logger.info("Added %d new Person objects" % p_count)
        return p_count

    def __get_by_uid(self, uid: str) -> Person:
        target_person = list(filter(lambda p: p.id == uid, self.people))

        if len(target_person) == 0:
            self.logger.error("Person:%s not found" % str(uid))
            raise PersonNotFound(uid)

        return target_person[0]

    def get(self, uid: str) -> Person:
        return self.__get_by_uid(uid)

    def kill(self, uid: str) -> None:
        person = self.__get_by_uid(uid)
        self.people.remove(person)

        person.alive = False
        self.people.add(person)
        self.logger.info("Person:$s unalived" % person.id)


class TownManager(ClassWithLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pueblos = set()

    def add(self, pueblo):
        self.pueblos.add(pueblo)

    def init_town_list(self):
        self.logger.info("Init town list OK")


class EventManager(ClassWithLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events = set()

    def init_event_list(self):
        self.logger.info("Init event list OK")
