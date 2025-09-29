from db import *;

class GameState:
    def __init__(self):
        self.id = None
        self.name = None
        self.starting_ICAO = None
        self.money = None
        self.co2_budget = None
        self.quota = None
        self.balance = None
        self.owned_airports = []

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

        
        