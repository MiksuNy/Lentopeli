from enum import Enum
from db import *
import random

class AirplaneManager:
    def __init__(self):
        self.all_planes = []
        self.db: Database = Database()
        self.db.connect()

    def spawn(self, amount):
        locations = self.db.query(f"SELECT name FROM airport WHERE type != 'heliport' OR 'closed' OR 'ballonport' ORDER BY RAND() LIMIT {amount};")
        for location in locations:
            self.all_planes.append(Airplane(random.choice(list(AirplaneType)), location))

    def move_all(self):
        destinations = self.db.query(f"SELECT name FROM airport WHERE type != 'heliport' OR 'closed' OR 'ballonport' ORDER BY RAND() LIMIT {len(self.all_planes)};")
        for i in range(len(destinations)):
            self.all_planes[i].location = destinations[i]

class AirplaneType(Enum):
    PASSENGER_PLANE = 0
    CARGO_PLANE = 1

class Airplane:
    def __init__(self, airplane_type, location = None):
        self.airplane_type = airplane_type
        self.location = location
        self.owned_by_player = False
