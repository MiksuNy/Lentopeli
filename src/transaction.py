from db import Database
import random

class TransactionManager:
    def __init__(self):
        self.db: Database = Database()
        self.db.connect()

    def check_game_exists(self, username) -> bool:
        exists = bool(self.db.query(f"SELECT id FROM game WHERE screen_name = '{username}';"))
        return exists
    
    def get_game_id(self, username) -> str:
        return self.db.query(f"SELECT id FROM game WHERE screen_name = '{username}'")

    def create_game(self, username) -> str:
        id = int(self.db.query("SELECT id FROM game ORDER BY CAST(id AS UNSIGNED) DESC LIMIT 1;")[0][0]) + 1
        starting_ICAO = self.db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]
        game_seed = random.getrandbits(64)
        self.db.query(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, balance, seed) VALUES ({id}, 0, 10000, '{starting_ICAO}', '{username}', 100000, {game_seed});")
        self.db.query(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{starting_ICAO}', '{id}');")

        return id
    
    def get_owned_airports(self, id):
        owned = []
        res = self.db.query(f"SELECT airport_ident FROM owns_airport WHERE game_id = '{id}';")
        print(f"SELECT airport_ident FROM owns_airport WHERE game_id = '{id}';")
        for ident in res:
            print(f"SELECT * FROM airport WHERE ident = '{ident[0]}';")
            owned.append(self.db.query(f"SELECT * FROM airport WHERE ident = '{ident[0]}';"))
        return owned
    
    def get_balance(self, id):
        balance = self.db.query(f"SELECT balance FROM game WHERE id = '{id}';")
        return balance

    def subtract_balance(self, id, amount):
        self.db.query(f"UPDATE game SET balance = balance - {amount} WHERE id = '{id}';")
    
    def add_balance(self, id, amount):
        self.db.query(f"UPDATE game SET balance = balance + {amount} WHERE id = '{id}';")

    def get_username(self, id):
        username = self.db.query(f"SELECT screen_name FROM game WHERE id='{id}';")
        return username