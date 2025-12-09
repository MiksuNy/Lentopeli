from db import *;
from state import *;
import random

class Airport:
    def __init__(self, ident, seed, db):
        self.name = None
        self.ident = None
        self.iso_country = None
        self.country = None
        self.cost = None
        self.type = None

        self.name, self.ident, self.iso_country, self.country, self.type = db.query(f"SELECT airport.name, airport.ident, airport.iso_country, country.name, airport.type FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{ident}';")[0]

        random.seed(bytes(seed) + bytes(self.ident, "utf-8"))
        self.cost = 10000 + random.randint(5000, 15000)

        price_ranges = {
            'small_airport': (10000, 50000),  # Price range in currency units
            'medium_airport': (50000, 130000),
            'large_airport': (130000, 250000)
        }

        if self.type in price_ranges:
            min_price, max_price = price_ranges[self.type]

        random_price = random.randint(min_price, max_price)
        self.cost = random_price
