import numpy as np

from backend.dto import GameGuessResponse, HintResponse, GamesResponse
from database.game_database import GameDatabase
from logic.daily_target_game import DailyTargetGame
from logic.game import Game
from logic.game_comparison import GameComparison
from logic.hint_generator import HintGenerator

METADATA_NAME = "metadata"
SCORE_NAME = "score"
VALUES_NAME = "values"


class Integration:
    def __init__(self, database: GameDatabase, hint_generator: HintGenerator):
        self._database = database
        self._hint_generator = hint_generator
        self._game_names = []

        self._game = self._new_game()

    def get_games(self) -> GamesResponse:
        games = self._get_game_names()
        return GamesResponse(games=games)

    def guess(self, game_name) -> GameGuessResponse:
        target_game_record = self._get_or_update_game().target_game

        print("Target:", target_game_record[METADATA_NAME]["Name"], "; Guess:", game_name)

        guessed_game_record = self._database.get_similarity(
            name=game_name, embedding=target_game_record[VALUES_NAME])

        if not guessed_game_record:
            return None
        
        game_comparison = self._compare_games(target_game_record[METADATA_NAME], guessed_game_record[METADATA_NAME])
        return GameGuessResponse(comparison=game_comparison, score=guessed_game_record[SCORE_NAME])

    def get_hint(self, game_name: str) -> HintResponse:
        hint = self._hint_generator.generate_hint(
            target_game_name=self._game.target_game[METADATA_NAME]["Name"], guessed_game_name=game_name)

        return HintResponse(hint=hint)

    def get_target_game():
        pass

    def _get_or_update_game(self) -> DailyTargetGame:
        if not self._game or self._game.is_expired():
            self._game = self._new_game()

        return self._game

    def _new_game(self) -> DailyTargetGame:
        game_names = self._get_game_names()
        any_game_name = np.random.choice(game_names)
        game = self._database.get_by_id(any_game_name)
        return DailyTargetGame(game)

    def _get_game_names(self) -> list[str]:
        if not self._game_names:
            self._game_names = self._database.get_ids()

        return self._game_names

    def _compare_games(self, base_metadata: dict, comparable_metadata: dict) -> GameComparison:
        target_game = Game.from_metadata(base_metadata)
        guessed_game = Game.from_metadata(comparable_metadata)

        return GameComparison(target_game, guessed_game)

