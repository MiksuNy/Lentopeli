import sys
import os

# Lisätään src kansio pythonin polkuun jotta importit toimii
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
from src.main import welcome_screen
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)


# Endpoint front-endista suoritettavalle loginille, palauttaa gamestaten
@app.route("/login/<username>", methods=["POST"])
@cross_origin()

def login(username: str):
    state = welcome_screen(username)
    return jsonify(state)


if __name__ == "__main__":
    app.run(debug=True)
