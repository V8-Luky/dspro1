"""The entry point and implementation of the backend API."""

from flask import Flask, Request, request
from flask_cors import CORS

from backend import Integration
from database import api_key as pinecone_api_key, GameDatabase
from genai import api_key as gemini_api_key
from logic import HintGenerator

# Constants
SUCCESS = 200
BAD_REQUEST = 400
NOT_FOUND = 404

NAME_QUERY = "name"

# Helper functions


def get_name_from_request(req: Request) -> str | None:
    """Extracts the name query parameter from the request."""
    if NAME_QUERY not in req.args:
        return None
    return req.args.get(NAME_QUERY).strip('"')


def get_no_name_error() -> tuple[str, int]:
    """Returns an error message for when the name query parameter is missing."""
    return 'Must provide a "name" query parameter', BAD_REQUEST


# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Initialize the integration
INDEXES = {"description-index": {"dimension": 768, "weight": 0.5},
           "tags-index": {"dimension": 300, "weight": 0.5}}

database = GameDatabase(api_key=pinecone_api_key, indexes={
                        index_name: index_value["dimension"] for index_name, index_value in INDEXES.items()})
hint_generator = HintGenerator(api_key=gemini_api_key)

integration = Integration(database=database, hint_generator=hint_generator, indexes={
                          index_name: index_value["weight"] for index_name, index_value in INDEXES.items()})

# The api endpoints


@app.route("/games", methods=["GET"])
def get_games():
    """Returns a list of all the games in the database."""
    return integration.get_games().to_json(), SUCCESS


@app.route("/hint", methods=["GET"])
def get_hint():
    """Returns a hint for the game with the provided name."""
    if (name := get_name_from_request(request)) is None:
        return get_no_name_error()

    hint = integration.get_hint(name)
    if not hint:
        return f"No hint for game with name {name} found", NOT_FOUND

    return hint.to_json(), SUCCESS


@app.route("/target", methods=["GET"])
def get_target_game():
    """Returns the target game that the player has to guess."""
    return integration.get_target_game().to_json(), SUCCESS


@app.route("/guess", methods=["POST"])
def guess_game():
    """Guesses the game with the provided name."""
    if (name := get_name_from_request(request)) is None:
        return get_no_name_error()

    guess_result = integration.guess(name)
    if not guess_result:
        return f"No game with name {name} found", NOT_FOUND

    return guess_result.to_json(), SUCCESS


if __name__ == '__main__':
    app.run(debug=False, port=8080, host="0.0.0.0")
