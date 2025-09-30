from db import *;

class GameState:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.starting_ICAO = None
        self.co2_budget = None
        self.quota = None
        self.balance = None
        self.owned_airports = []

        self.db: Database = Database()
        self.db.connect()

        self.name, self.co2_consumed, self.co2_budget, self.quota, self.balance = self.db.query(f"SELECT screen_name, co2_consumed, co2_budget, quota, balance FROM game WHERE id = '{id}';")[0]

class Wallet(GameState):
    def __init__(self):
        self.db: Database = Database
        self.db.connect()


    def subtract(self, amount):
        super.money -= amount
        self.db.query(f"UPDATE game SET balance = balance - {amount} WHERE id = '{super.id}';")
    
    def add(self, amount):
        super.money += amount
        self.db.query(f"UPDATE game SET balance = balance + {amount} WHERE id = '{super.id}';")
    
    def get_balance(self):
        return self.db.query(f"SELECT balance FROM game WHERE id = '{super.id}';")[0][0]

        
        
