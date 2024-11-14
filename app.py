from flask import Flask, request, jsonify
from backend.integration import Integration
from database.game_database import GameDatabase

app = Flask(__name__)

API_KEY = "3ba8f200-99a7-4b16-8d49-ba671878b6d9"  # Yeah, security
DIMENSIONALITY = 384

database = GameDatabase(api_key=API_KEY, dimension=DIMENSIONALITY)
integration = Integration(database=database)

SUCCESS = 200
BAD_REQUEST = 400
NOT_FOUND = 404

NAME_QUERY = "name"


@app.route('/guess', methods=["POST"])
def guess_game():
    if NAME_QUERY not in request.args:
        return "Must provide a \"name\" query parameter", BAD_REQUEST

    name = request.args.get("name").strip("\"")
    guess_result = integration.guess(name)
    if not guess_result:
        return f"No game with name {name} found", NOT_FOUND

    return jsonify(guess_result.to_json()), SUCCESS


@app.route('/games', methods=["GET"])
def get_games():
    return jsonify(integration.get_games()), SUCCESS


if __name__ == '__main__':
    app.run(debug=True)
