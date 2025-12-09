from airplane import AirplaneType
from db import Database
import random

class TransactionManager:
    def __init__(self):
        self.db: Database = Database()

        self.list_icao = self.db.query_all("SELECT ident FROM airport;")

    def check_game_exists(self, username) -> bool:
        exists = bool(self.db.query_all(f"SELECT id FROM game WHERE screen_name = '{username}';"))
        return exists
    
    def get_game_id(self, username) -> str:
        return self.db.query_all(f"SELECT id FROM game WHERE screen_name = '{username}'")

    def create_game(self, username) -> str:
        id = int(self.db.query_all("SELECT id FROM game ORDER BY CAST(id AS UNSIGNED) DESC LIMIT 1;")[0][0]) + 1
        starting_ICAO = self.db.query_all("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]
        game_seed = random.getrandbits(64)
        self.db.execute(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, balance, seed) VALUES ({id}, 0, 10000, '{starting_ICAO}', '{username}', 100000, {game_seed});")
        self.db.execute(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{starting_ICAO}', '{id}');")

        return id
    
    def get_owned_airports(self, id):
        owned = []
        res = self.db.query_all(f"SELECT airport_ident FROM owns_airport WHERE game_id = '{id}';")
        for ident in res:
            owned.append(self.db.query_all(f"SELECT * FROM airport WHERE ident = '{ident[0]}';"))
        return owned
    
    def get_random_set_airports(self):
        return self.db.query_all("SELECT * FROM airport ORDER BY RAND() LIMIT 100;")
    
    def get_balance(self, id):
        balance = self.db.query_all(f"SELECT balance FROM game WHERE id = '{id}';")
        return balance

    def subtract_balance(self, id, amount):
        self.db.execute(f"UPDATE game SET balance = balance - {amount} WHERE id = '{id}';")
    
    def add_balance(self, id, amount):
        self.db.execute(f"UPDATE game SET balance = balance + {amount} WHERE id = '{id}';")

    def get_username(self, id):
        username = self.db.query_all(f"SELECT screen_name FROM game WHERE id='{id}';")
        return username
    
    def create_airplanes(self, game_id, amount):
        for _ in range(amount):
            try:
                airplane_id = int(self.db.query_all("SELECT id FROM airplane ORDER BY CAST(id AS UNSIGNED) DESC LIMIT 1;")[0][0]) + 1
            except:
                airplane_id = 1
            airplane_type = random.choice(list(AirplaneType))
            price = random.randint(500, 1500)
            self.db.execute(
                f"INSERT INTO airplane (id, game_id, airplane_type, price) VALUES ('{airplane_id}', '{game_id}', '{airplane_type}', {price});"
            )

    def buy_airplane(self, game_id, airplane_id) -> bool:
        price = self.db.query_all(f"SELECT price FROM airplane WHERE id = '{airplane_id}'")[0]
        if self.get_balance() >= price:
            self.db.execute(f"INSERT INTO owns_airplane (airplane_id, game_id) VALUES ('{airplane_id}', '{game_id}');")
            self.subtract_balance(id, price)
            return True
        else:
            return False
    
    def get_available_airplanes(self, id):
        return self.db.query_all(f"SELECT * FROM airplane WHERE game_id = '{id}';")

    def buy_airport(self, id, airport_ident):
        if not self.validate_icao(airport_ident):
            return False
        seed = self.db.query_all(f"SELECT seed FROM game WHERE id='{id}';")[0][0]
        random.seed(bytes(seed) + bytes(airport_ident, "utf-8"))
        price = 10000 + random.randint(5000, 15000)
        if self.get_balance(id)[0][0] >= price:
            self.db.execute(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{airport_ident}', '{id}');")
            self.subtract_balance(id, price)
            return True
        else:
            return False
    
    def get_airport_price(self, id, airport_ident):
        if not self.validate_icao(airport_ident):
            return False
        seed = self.db.query_all(f"SELECT seed FROM game WHERE id='{id}';")[0][0]
        random.seed(bytes(seed) + bytes(airport_ident, "utf-8"))
        price = 10000 + random.randint(5000, 15000)
        return price

    def validate_icao(self, icao) -> bool:
        if len(icao) != 4:
            return False
        if (icao,) not in self.list_icao:
            return False
        return True

    def next_turn(self, game_id):
        self.db.query_all(f"UPDATE game SET turns = turns + 1 WHERE id = '{game_id}';")

        airplane_count = self.db.query_all(f"SELECT COUNT(*) FROM owns_airplane WHERE game_id = '{game_id}'")[0]
        for _ in airplane_count:
            random_ICAO = self.db.query_all("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]
            self.db.execute(f"UPDATE airplane SET airport_ident = '{random_ICAO}' WHERE game_id = '{game_id}'")
    
    def check_pool_health(self):
        return self.db.check_pool_health()
