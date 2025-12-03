import random
from flask import Flask
from flask_cors import CORS, cross_origin
from state import GameState

app = Flask(__name__)
cors = CORS(app)

state = GameState()



# Endpoint front-endista suoritettavalle loginille, palauttaa gamestaten
@app.route("/login/<username>", methods=["POST"])
@cross_origin()
def login(login_name: str = "") -> dict:
    state = state.init_game(login_name)

    
    location = state.db.query(f"SELECT location FROM game WHERE screen_name = '{login_name}';")
    
    if is_returning_user:
        state.name, state.co2_consumed, state.co2_budget, state.quota, state.seed = state.db.query(f"SELECT screen_name, co2_consumed, co2_budget, quota, seed FROM game WHERE id = '{id}';")[0]
        return state
    else:
        id = int(state.db.query("SELECT id FROM game ORDER BY id DESC LIMIT 1;")[0][0]) + 1
        starting_ICAO = state.db.query("SELECT ident FROM airport WHERE type = 'small_airport' ORDER BY RAND() LIMIT 1;")[0][0]
        game_seed = random.getrandbits(64)
        state.db.query(f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, balance, seed) VALUES ({id}, 0, 10000, '{starting_ICAO}', '{login_name}', 100000, {game_seed});")
        state.db.query(f"INSERT INTO owns_airport (airport_ident, game_id) VALUES('{starting_ICAO}', '{id}');")
        starting_port_meta = state.db.query(f"SELECT airport.name, country.name FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE ident = '{starting_ICAO}';")
        # Luodaan palautettava gamestate jos käyttäjä on uusi pelaaja
        try:

        except Exception as e:
            return {"Exception": e}
        GameState(id)
        return game_state_dict


if __name__ == "__main__":
    app.run(debug=True)