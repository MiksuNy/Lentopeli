from db import *;
from state import GameState;

class AirportManager:
    def __init__(self):
        self.no_fly_zones = None
        self.db: Database = Database()
        self.db.connect()
    
    def get_owned(self, game_id, seed=0):
        owned = []
        res = self.db.query(f"SELECT airport_ident FROM owns_airport WHERE game_id = '{game_id}';")
        for i in range(len(res)):
            airport: Airport = Airport(res[i][0], seed)
            owned.append(airport)
        return owned

    def buy(self, ident, game_id):

        if self.db.query(f"SELECT ident FROM airport WHERE ident = '{ident}';"):
            item: Airport = Airport(ident)
            balance = GameState(game_id).wallet.balance
            if item.cost <= balance:
                self.db.query(f"INSERT INTO owns_airport (game_id, airport_ident) VALUES ({game_id}, '{ident}');")
                print(f"Congratulations, you now own {self.db.query(f"SELECT name FROM airport WHERE ident = '{ident}';")[0][0]}.")
            else:
                print("Sorry, you cannot afford this right now.")
        else:
            print("Sorry, not such airport exists...")
    


class Airport(AirportManager):
    def __init__(self, ident, seed):
        super().__init__()
        import random

        self.name = None
        self.ident = None
        self.iso_country = None
        self.country = None
        self.cost = None
        self.type = None

        self.name, self.ident, self.iso_country, self.country, self.type = self.db.query(f"SELECT airport.name, airport.ident, airport.iso_country, country.name, airport.type FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{ident}';")[0]

        random.seed(bytes(seed) + bytes(self.ident, "utf-8"))
        self.cost = 10000 + random.randint(5000, 15000)

        self.cost =  0#TODO: implement an algorithm that deterministically calculates a price for airports based on a seed unique to each GameState