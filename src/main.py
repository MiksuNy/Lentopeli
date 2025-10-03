from airplane import AirplaneManager
from db import *;
from event import *;
from state import *;
from airport import *;
from command import Command



def welcome_screen() -> GameState:
    login_name = input("Username: ")
    is_returning_user = db.query(f"SELECT screen_name, id FROM game WHERE screen_name = '{login_name}';")

    if is_returning_user:
        state = GameState(is_returning_user[0][1])
        print(f"Welcome back, {state.name}!")
        return state
    else:
        print(f"Welcome, {login_name}!")
        print("Starting new game...")
        
        id = int(db.query("SELECT id FROM game ORDER BY id DESC LIMIT 1;")[0][0]) + 1
        starting_ICAO = db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]

        db.query(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, balance) VALUES ({id}, 0, 10000, '{starting_ICAO}', '{login_name}', 100000);")
        db.query(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{starting_ICAO}', '{id}');")
        starting_port_meta = db.query(f"SELECT airport.name, country.name FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{starting_ICAO}';")

        print(f"Congratulations, your business has been granted an operating license at the {starting_port_meta[0][0]}, {starting_port_meta[0][1]}.")
        return GameState(id)
    

db: Database = Database()
db.connect()

event_manager: EventManager = EventManager()
airplane_manager: AirplaneManager = AirplaneManager()

airplane_manager.spawn(10)

state = welcome_screen()


# EVENT LOOP:
should_quit = False
while should_quit == False:
    input_string = input("Give a command: ")
    command = Command(input_string)
    command.run(state)
