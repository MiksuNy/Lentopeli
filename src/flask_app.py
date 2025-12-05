from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from state import GameState

app = Flask(__name__)
cors = CORS(app)

state = GameState()



# Endpoint front-endista suoritettavalle loginille, palauttaa gamestaten
@app.route("/login/<username>", methods=["POST"])
@cross_origin()
def login(login_name: str):
    return state.init_game(login_name)



@app.route("/airports/getAll", methods=["GET"])
@cross_origin()
def get_all_airports():
    return jsonify(state.get_all_airports())

@app.route("/airports/getOwned", methods=["GET"])
@cross_origin()
def get_owned_airports():
    return jsonify(state.get_owned_airports())



@app.route("/balance/get", methods=["GET"])
@cross_origin()
def get_balance():
    return jsonify(state.get_balance())

@app.route("/balance/add/<int:amount>", methods=["POST"])
@cross_origin()
def add_balance(amount: int):
    state.add_balance(amount)

@app.route("/balance/subtract/<int:amount>", methods=["POST"])
@cross_origin()
def subtract_balance(amount: int):
    state.subtract_balance(amount)



@app.route("/player/getScreenName", methods=["GET"])
@cross_origin()
def get_screen_name():
    return jsonify(state.get_screen_name())



if __name__ == "__main__":
    app.run(debug=True)