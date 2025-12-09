from db import *
from enum import Enum
import random

# Value is chance to execute event (0: no chance, 100: always happens)
class Event(Enum):
    NO_FLY_ZONE = 5
    AIRPORT_QUARANTINE = 10
    AIRPLANE_FAULT = 15

class EventManager:
    def __init__(self):
        self.db: Database = Database()
        self.db.connect()

    def roll(self):
        event = random.choice(list(Event))
        chance = random.randint(0, 100)
        if event.value >= chance:
            match event:
                case Event.NO_FLY_ZONE:
                    country_name = self.db.query("SELECT name FROM country ORDER BY RAND() LIMIT 1")[0][0]
                    print(f"No Fly Zone triggered for {country_name}")
                case Event.AIRPORT_QUARANTINE:
                    airport_name = self.db.query("SELECT name FROM airport ORDER BY RAND() LIMIT 1")[0][0]
                    print(f"Quarantine triggered for {airport_name}")
                case Event.AIRPLANE_FAULT:
                    pass
