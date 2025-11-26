import sys
import os

# Lisätään src kansio pythonin polkuun jotta importit toimii
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
from src.main import welcome_screen
from flask import Flask

app = Flask(__name__)

@app.route("/login/<username>")
def login(username: str):
    return username

if __name__ == "__main__":
    app.run(debug=True)
