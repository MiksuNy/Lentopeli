from db import *;

class GameState:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.starting_ICAO = None
        self.co2_budget = None
        self.quota = None
        self.wallet = None
        self.owned_airports = []

        self.db: Database = Database()
        self.db.connect()

        self.name, self.co2_consumed, self.co2_budget, self.quota = self.db.query(f"SELECT screen_name, co2_consumed, co2_budget, quota FROM game WHERE id = '{id}';")[0]
        self.wallet = Wallet(self.id)

class Wallet(GameState):
    def __init__(self, game_id):
        self.db: Database = Database()
        self.db.connect()

        self.balance = self.db.query(f"SELECT balance FROM game WHERE id = '{game_id}';")


    def subtract(self, amount):
        super.money -= amount
        self.db.query(f"UPDATE game SET balance = balance - {amount} WHERE id = '{super.id}';")
    
    def add(self, amount):
        super.money += amount
        self.db.query(f"UPDATE game SET balance = balance + {amount} WHERE id = '{super.id}';")
    
    def get_balance(self):
        return self.db.query(f"SELECT balance FROM game WHERE id = '{super.id}';")[0][0]

        
