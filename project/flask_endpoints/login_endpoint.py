import sys
import os

# Lisätään src kansio pythonin polkuun jotta importit toimii
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
from src.main import welcome_screen
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/login/<username>", methods=["POST", "GET"])
def login(username: str):
    state = welcome_screen(username)
    print(state.id, state.name, state.wallet.balance, state.co2_budget, state.co2_consumed)
    return jsonify(state)


if __name__ == "__main__":
    app.run(debug=True)
