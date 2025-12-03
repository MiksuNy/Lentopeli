from airport import *
from command import Command
import random

# login_name parametrille arvo tulee front-endiltä
def init_game(login_name: str = "") -> dict:
    db: Database = Database()
    db.connect()

    is_returning_user = db.query(f"SELECT screen_name, id FROM game WHERE screen_name = '{login_name}';")
    location = db.query(f"SELECT location FROM game WHERE screen_name = '{login_name}';")
    if is_returning_user:
        state = GameState(is_returning_user[0][1])
        print(f"Welcome back, {state.name}!")

        # Määritellään palautettava gamestate jos käyttäjä jatkaa aiempaa peliä
        try:
            game_state_dict = {
                "newUser": False,
                "gameState": {
                    "name": state.name,
                    "id": state.id,
                    "co2Consumed": state.co2_consumed,
                    "co2Budget": state.co2_budget,
                    "startingIcao": location[0][0],
                    "startingPortMeta": {
                        "airportName": None,
                        "countryName": None
                    },
                    "quota": state.quota,
                    "balance": state.wallet.balance[0][0] if state.wallet.balance[0][0] else 0,
                    "messages": [
                        {
                            "type": "info",
                            "text": f"Welcome back, {state.name}!"
                        }
                    ],
                    "ownsAirport": state.airplane_manager.get_owned() if True else None
                }
            }
        except Exception as e:
            return {"Exception": e}

        return game_state_dict

    else:
        print(f"Welcome, {login_name}!")
        print("Starting new game...")
        
        id = int(db.query("SELECT id FROM game ORDER BY id DESC LIMIT 1;")[0][0]) + 1
        starting_ICAO = db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]

        game_seed = random.getrandbits(64)

        db.query(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, balance, seed) VALUES ({id}, 0, 10000, '{starting_ICAO}', '{login_name}', 100000, {game_seed});")
        db.query(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{starting_ICAO}', '{id}');")
        starting_port_meta = db.query(f"SELECT airport.name, country.name FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{starting_ICAO}';")

        print(f"Congratulations, your business has been granted an operating license at the {starting_port_meta[0][0]}, {starting_port_meta[0][1]}.")

        # Luodaan palautettava gamestate jos käyttäjä on uusi pelaaja
        try:
            game_state_dict = {
                "newUser": True,
                "gameState": {
                    "name": login_name,
                    "id": id,
                    "co2Consumed": 0,
                    "co2Budget": 10000,
                    "startingIcao": starting_ICAO,
                    "startingPortMeta": {
                        "airportName": starting_port_meta[0][0],
                        "countryName": starting_port_meta[0][1]
                    },
                    "quota": "",
                    "balance": 100000,
                    "messages": [
                        {
                            "type": "info",
                            "text": f"Congratulations, your business has been granted an operating license at the {starting_port_meta[0][0]}, {starting_port_meta[0][1]}."
                        }
                    ],
                    "ownsAirport": None
                }
            }
        except Exception as e:
            return {"Exception": e}

        GameState(id)
        return game_state_dict