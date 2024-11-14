from backend.game_guess_response import GameGuessResponse
from database.game_database import GameDatabase
from logic.daily_game import DailyGame


class Integration:
    def __init__(self, database: GameDatabase):
        self._database = database
        self._game = self._new_game()

    def get_games(self):
        return self._database.get_ids()

    def guess(self, game_name):
        target_game = self._get_or_update_game().target_game

        print("Target:", target_game["metadata"]["name"])
        print("Guess:", game_name)

        result = self._database.get_similarity(
            name=game_name, embedding=target_game["values"])

        if not result:
            return None

        return GameGuessResponse(metadata=result["metadata"], score=result["score"])

    def _get_or_update_game(self) -> DailyGame:
        if not self._game or self._game.is_expired():
            self._game = self._new_game()

        return self._game

    def _new_game(self) -> DailyGame:
        return DailyGame(self._database.get_random())
