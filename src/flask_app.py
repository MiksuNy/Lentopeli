from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from db import *;
from main import init_game
app = Flask(__name__)
cors = CORS(app)
db = Database()
db.connect()



# Endpoint front-endista suoritettavalle loginille, palauttaa gamestaten
@app.route("/login/<username>", methods=["POST"])
@cross_origin()
def login(username: str):
    state = init_game(username)
    return jsonify(state)



if __name__ == "__main__":
    app.run(debug=True)