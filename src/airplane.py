import random
from enum import Enum
from db import *
from state import *

class AirplaneManager:
    def __init__(self):
        self.airplanes = []
        self.db: Database = Database()
        self.db.connect()

    def spawn(self, amount):
        locations = self.db.query(f"SELECT name FROM airport WHERE type != 'heliport' OR 'closed' OR 'ballonport' ORDER BY RAND() LIMIT {amount};")
        for location in locations:
            self.airplanes.append(Airplane(random.choice(list(AirplaneType)), location))

    def buy(self, airplane_type, game_state):
        cost = 1000 # Hard coded value for now, replace this with actual airplane costs
        owned_airports = game_state.airport_manager.get_owned(game_state)
        if owned_airports == None:
            print("You need to own an airport to buy airplanes!")
        elif game_state.wallet.get_balance() >= cost:
            self.airplanes.append(Airplane(airplane_type, owned_airports[0], True))

    def move_all(self):
        destinations = self.db.query(f"SELECT name FROM airport WHERE type != 'heliport' OR 'closed' OR 'ballonport' ORDER BY RAND() LIMIT {len(self.all_airplanes)};")
        for i in range(len(destinations)):
            self.airplanes[i].location = destinations[i]

    def get_owned(self):
        return [item for item in self.airplanes if item.owned_by_player == True]

class AirplaneType(Enum):
    PASSENGER = "passenger"
    CARGO = "cargo"

class Airplane:
    def __init__(self, airplane_type, location = None, owned_by_player = False):
        self.airplane_type = airplane_type
        self.location = location
        self.owned_by_player = owned_by_player
