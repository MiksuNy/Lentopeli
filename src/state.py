import random
from airplane import AirplaneManager
from airport import AirportManager
from db import Database
from event import EventManager


class GameState:
    def __init__(self):
        self.id = id
        self.name = None
        self.starting_ICAO = None
        self.co2_budget = None
        self.quota = None
        self.balance = None
        self.seed = None

        self.event_manager = EventManager()
        self.airport_manager = AirportManager()
        self.airplane_manager = AirplaneManager()

        self.db: Database = Database()
        self.db.connect()
    
    def init_game(self, login_name) -> dict:
        is_returning_user = self.db.query(f"SELECT screen_name, id FROM game WHERE screen_name = '{login_name}';")
        if is_returning_user:
            self.name, self.co2_consumed, self.co2_budget, self.quota, self.seed = self.db.query(f"SELECT screen_name, co2_consumed, co2_budget, quota, seed FROM game WHERE id = '{is_returning_user[0][1]}';")[0]
            
            game_state_dict = {
                "newUser": False,
                "gameState": {
                    "name": self.name,
                    "id": self.id,
                    "co2Consumed": self.co2_consumed,
                    "co2Budget": self.co2_budget,
                    "quota": self.quota,
                    "balance": self.get_balance(),
                    "ownedAirplanes": None,
                    "ownedAirports": None
                }
            }
            return game_state_dict
        else:
            id = int(self.db.query("SELECT id FROM game ORDER BY id DESC LIMIT 1;")[0][0]) + 1
            starting_ICAO = self.db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]
            game_seed = random.getrandbits(64)
            self.db.query(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, balance, seed) VALUES ({id}, 0, 10000, '{starting_ICAO}', '{login_name}', 100000, {game_seed});")
            self.db.query(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{starting_ICAO}', '{id}');")
            starting_port_meta = self.db.query(f"SELECT airport.name, country.name FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{starting_ICAO}';")
            
            game_state_dict = {
                "newUser": True,
                "gameState": {
                    "name": login_name,
                    "id": id,
                    "co2Consumed": 0,
                    "co2Budget": 10000,
                    "quota": "",
                    "balance": 100000,
                    "ownedAirplanes": None,
                    "ownedAirports": self.airport_manager.airports.append(self.db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0])
                }
            }
        return self

    def subtract_balance(self, amount):
        self.db.query(f"UPDATE game SET balance = balance - {amount} WHERE id = '{self.id}';")
    
    def add_balance(self, amount):
        self.db.query(f"UPDATE game SET balance = balance + {amount} WHERE id = '{self.id}';")
    
    def get_balance(self):
        return self.db.query(f"SELECT balance FROM game WHERE id = '{self.id}';")[0][0]
    
    def get_screen_name(self):
        return self.db.query(f"SELECT screen_name FROM game WHERE id = '{self.id}';")[0][0]