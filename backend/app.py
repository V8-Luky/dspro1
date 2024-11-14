from flask import Flask
from backend.integration import Integration
from database.game_database import GameDatabase

app = Flask(__name__)

API_KEY = "3ba8f200-99a7-4b16-8d49-ba671878b6d9"  # Yeah, security
DIMENSIONALITY = 384

database = GameDatabase(api_key=API_KEY, dimension=DIMENSIONALITY)
integration = Integration(database=database)


@app.route('/guess/<game_name>')
def guess(game_name):
    integration.guess(game_name)
    return f"Guessing game {game_name}"


@app.route('/list')
def list():
    integration.get_list()
    return "Listing all games"
