from db import *;
from airport import AirportManager
from airplane import AirplaneManager
from event import *

class GameState:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.starting_ICAO = None
        self.co2_budget = None
        self.quota = None
        self.wallet = None
        self.seed = None

        self.event_manager = EventManager()
        self.airport_manager = AirportManager()
        self.airplane_manager = AirplaneManager()
        self.airplane_manager.spawn(100)

        self.db: Database = Database()
        self.db.connect()

        self.name, self.co2_consumed, self.co2_budget, self.quota, self.seed = self.db.query(f"SELECT screen_name, co2_consumed, co2_budget, quota, seed FROM game WHERE id = '{id}';")[0]
        self.wallet = Wallet(self.id)

class Wallet(GameState):
    def __init__(self, game_id):
        self.db: Database = Database()
        self.db.connect()

        self.id = game_id

        self.balance = self.db.query(f"SELECT balance FROM game WHERE id = '{self.id}';")


    def subtract(self, amount):
        super.money -= amount
        self.db.query(f"UPDATE game SET balance = balance - {amount} WHERE id = '{self.id}';")
    
    def add(self, amount):
        super.money += amount
        self.db.query(f"UPDATE game SET balance = balance + {amount} WHERE id = '{self.id}';")
    
    def get_balance(self):
        return self.db.query(f"SELECT balance FROM game WHERE id = '{self.id}';")[0][0]

        
