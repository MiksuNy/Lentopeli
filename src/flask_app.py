from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from state import GameState
from transaction import TransactionManager

app = Flask(__name__)
cors = CORS(app)

trmg = TransactionManager()

EXEMPT_ENDPOINTS = {'login', 'airports_random'}

@app.before_request
def middleware():
    if request.endpoint in EXEMPT_ENDPOINTS:
        return
    if not request.view_args or 'id' not in request.view_args:
        return jsonify({"error": "missing required argument [id]"}), 400

# Endpoint front-endista suoritettavalle loginille, palauttaa gamestaten
@app.route("/login/<username>", methods=["POST"], endpoint='login')
@cross_origin()
def login(username: str):
    if not trmg.check_game_exists(username):
        trmg.create_game(username)
    return trmg.get_game_id(username), 200




@app.route("/airports/getRandomSet", methods=["GET"], endpoint='airports_random')
@cross_origin()
def get_all_airports():
    print(trmg.get_random_set_airports())
    return jsonify(trmg.get_random_set_airports()), 200



@app.route("/balance/get/<id>", methods=["GET"])
@cross_origin()
def get_balance(id: int):
    return jsonify(trmg.get_balance(id)), 200

@app.route("/balance/add/<int:amount>/<id>", methods=["POST"])
@cross_origin()
def add_balance(amount: int, id: int):
    trmg.add_balance(id, amount)
    return Response('', status=200)

@app.route("/balance/subtract/<int:amount>/<id>", methods=["POST"])
@cross_origin()
def subtract_balance(amount: int, id: int):
    trmg.subtract_balance(id, amount)
    return Response('', status=200)



@app.route("/player/getScreenName/<id>", methods=["GET"])
@cross_origin()
def get_screen_name(id: int):
    return jsonify(trmg.get_username(id)), 200



@app.route("/airplanes/create/<int:amount>/<id>", methods=["POST"])
@cross_origin()
def create_airplanes(amount: int, id: int):
    trmg.create_airplanes(id, amount)
    return Response('', status=200)

@app.route("/airplanes/buy/<airplane_id>/<id>", methods=["POST"])
@cross_origin()
def buy_airplane(airplane_id: int, id: int):
    if trmg.buy_airplane(id, airplane_id):
        return Response('', status=200)
    else:
        return Response('Insufficient funds or bad airplane ID\n', status=403)
        

@app.route("/airports/buy/<airport_ident>/<id>", methods=["POST"])
@cross_origin()
def buy_airport(airport_ident: str, id: int):
    if trmg.buy_airport(id, airport_ident):
        return Response('', status=200)
    else:
        return Response('Insufficient funds or bad airport ID\n', status=403)

@app.route("/airports/getOwned/<id>", methods=["GET"])
@cross_origin()
def get_owned_airports(id: int):
    return jsonify(trmg.get_owned_airports(id)), 200

@app.route("/game/nextTurn/<id>", methods=["POST"])
@cross_origin()
def next_turn(id: int):
    trmg.next_turn(id)
    return Response('', status=200)



if __name__ == "__main__":
    app.run(debug=True)