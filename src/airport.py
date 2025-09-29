from db import *;

class AirportManager:
    def __init__(self):
        self.no_fly_zones = None
        self.db: Database = Database()
        self.db.connect()
    
    def get_owned(self, game_id):
        owned = []
        res = self.db.query(f"SELECT airport_ident FROM owns_airport WHERE game_id = '{game_id}';")
        for i in range(len(res)):
            airport: Airport = Airport(res[i][0])
            owned.append(airport)
        return owned

    def buy(self, ident, balance, game_id):
        item: Airport = Airport(ident)
        if item.cost <= balance:
            db.query(f"INSERT INTO owns_airport (game_id, airport_ident) VALUES ({game_id}, {ident});")

class Airport(AirportManager):
    def __init__(self, ident):
        super().__init__()
        self.name = None
        self.ident = None
        self.iso_country = None
        self.country = None
        self.cost = None
        self.type = None

        self.name, self.ident, self.iso_country, self.country, self.cost, self.type = self.db.query(f"SELECT airport.name, airport.ident, airport.iso_country, country.name, airport.cost, airport.type FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{ident}';")[0]

