from db import *;
from state import *;
from airport import *;



def welcome_screen():
    state.name = input("Username: ")
    is_returning_user = db.query(f"SELECT screen_name FROM game WHERE screen_name = '{state.name}';")

    if is_returning_user:
        state.id, state.co2_consumed, state.co2_budget = db.query(f"SELECT id, co2_consumed, co2_budget FROM game WHERE screen_name = '{state.name}';")[0]
        print(f"Welcome back, {state.name}!")
    else:
        print(f"Welcome, {state.name}!")
        print("Starting new game...")
        
        state.id = int(db.query("SELECT id FROM game ORDER BY id DESC LIMIT 1;")[0][0]) + 1
        state.co2_budget = 10000
        state.starting_ICAO = db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]

        res = db.query(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name) VALUES ({state.id}, 0, {state.co2_budget}, '{state.starting_ICAO}', '{state.name}');")
        res = db.query(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{state.starting_ICAO}', '{state.id}');")
        starting_port_meta = db.query(f"SELECT airport.name, country.name FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{state.starting_ICAO}';")

        print(f"Congratulations, your business has been granted an operating license at the {starting_port_meta[0][0]}, {starting_port_meta[0][1]}.")

    

db: Database = Database()
db.connect()

state: GameState = GameState


welcome_screen()
airport_manager: AirportManager = AirportManager()
state.owned_airports = airport_manager.get_owned(state.id)
print("\nYou currently own the following airports:")
for i in range(len(state.owned_airports)):
    print(f"{state.owned_airports[i].country}: {state.owned_airports[i].name} [{state.owned_airports[i].ident}]")
    