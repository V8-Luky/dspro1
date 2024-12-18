from flask import Flask, Request, request
from flask_cors import CORS
from backend.integration import Integration
from database.api_key import api_key as pinecone_api_key
from database.game_database import GameDatabase
from genai.api_key import api_key as gemini_api_key
from logic.hint_generator import HintGenerator

app = Flask(__name__)
CORS(app)

database = GameDatabase(api_key=pinecone_api_key, indexes={"description-index": 768, "tags-index": 300})
hint_generator = HintGenerator(api_key=gemini_api_key)

integration = Integration(database=database, hint_generator=hint_generator)

SUCCESS = 200
BAD_REQUEST = 400
NOT_FOUND = 404

NAME_QUERY = "name"


def get_name_from_request(req: Request) -> str | None:
    if NAME_QUERY not in req.args:
        return None
    return req.args.get(NAME_QUERY).strip('"')


def get_no_name_error() -> tuple[str, int]:
    return 'Must provide a "name" query parameter', BAD_REQUEST


@app.route("/guess", methods=["POST"])
def guess_game():
    if (name := get_name_from_request(request)) is None:
        return get_no_name_error()

    guess_result = integration.guess(name)
    if not guess_result:
        return f"No game with name {name} found", NOT_FOUND

    return guess_result.to_json(), SUCCESS


@app.route("/games", methods=["GET"])
def get_games():
    return integration.get_games().to_json(), SUCCESS


@app.route("/hint", methods=["GET"])
def get_hint():
    if (name := get_name_from_request(request)) is None:
        return get_no_name_error()

    hint = integration.get_hint(name)
    if not hint:
        return f"No hint for game with name {name} found", NOT_FOUND

    return hint.to_json(), SUCCESS

@app.route("/target", methods=["GET"])
def get_target_game():
    return integration.get_target_game().to_json(), SUCCESS


if __name__ == '__main__':
    app.run(debug=False, port=8080, host="0.0.0.0")
