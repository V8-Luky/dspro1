from backend.dto import GameGuessResponse, HintResponse, GamesResponse

from database.game_database import GameDatabase
from logic.daily_game import DailyGame
from logic.hint_generator import HintGenerator


class Integration:
    def __init__(self, database: GameDatabase, hint_generator: HintGenerator):
        self._database = database
        self._hint_generator = hint_generator
        self._game_names = []

        self._game = self._new_game()

    def get_games(self) -> GamesResponse:
        if not self._game_names:
            self._game_names = self._database.get_ids()
        
        return GamesResponse(games=self._game_names)

    def guess(self, game_name) -> GameGuessResponse:
        target_game = self._get_or_update_game().target_game

        print("Target:", target_game["metadata"]["Name"])
        print("Guess:", game_name)

        result = self._database.get_similarity(
            name=game_name, embedding=target_game["values"])

        if not result:
            return None

        return GameGuessResponse(metadata=result["metadata"], score=result["score"])

    def get_hint(self, game_name: str) -> HintResponse:
        hint = self._hint_generator.generate_hint(
            target_game_name=self._game.target_game["metadata"]["Name"], guessed_game_name=game_name)

        return HintResponse(hint=hint)

    def get_target_game():
        pass

    def _get_or_update_game(self) -> DailyGame:
        if not self._game or self._game.is_expired():
            self._game = self._new_game()

        return self._game

    def _new_game(self) -> DailyGame:
        return DailyGame(self._database.get_random())
