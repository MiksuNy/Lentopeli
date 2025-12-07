from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from state import GameState
from transaction import TransactionManager

app = Flask(__name__)
cors = CORS(app)

trmg = TransactionManager()

@app.before_request
def middleware():
    if request.endpoint in ['exempt_route']:
        return
    print(request.view_args)
    if not request.view_args or 'id' not in request.view_args:
        return jsonify({"error": "missing required argument [id]"}), 400

# Endpoint front-endista suoritettavalle loginille, palauttaa gamestaten
@app.route("/login/<username>", methods=["POST"], endpoint='exempt_route')
@cross_origin()
def login(username: str):
    if not trmg.check_game_exists(username):
        trmg.create_game(username)
    return trmg.get_game_id(username), 200



# funktio palauttaa niin ison listan et selain jäätyy

# @app.route("/airports/getAll", methods=["GET"])
# @cross_origin()
# def get_all_airports():
#     return jsonify(state.get_all_airports())

@app.route("/airports/getOwned/<id>", methods=["GET"])
@cross_origin()
def get_owned_airports(id):
    return jsonify(trmg.get_owned_airports(id)), 200



@app.route("/balance/get/<id>", methods=["GET"])
@cross_origin()
def get_balance(id):
    return jsonify(trmg.get_balance(id)), 200

@app.route("/balance/add/<int:amount>", methods=["POST"])
@cross_origin()
def add_balance(amount: int):
    trmg.add_balance(request.headers.get("id"), amount)
    return Response('', status=200)

@app.route("/balance/subtract/<int:amount>", methods=["POST"])
@cross_origin()
def subtract_balance(amount: int):
    trmg.subtract_balance(request.headers.get("id"), amount)
    return Response('', status=200)



@app.route("/player/getScreenName", methods=["GET"])
@cross_origin()
def get_screen_name():
    return jsonify(trmg.get_username(request.headers.get("id"))), 200



if __name__ == "__main__":
    app.run(debug=True)