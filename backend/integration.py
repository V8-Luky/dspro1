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

INDEXES = {
    "description-index": 0.5,
    "tags-index": 0.5
}


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
        scores = list()
        weights = list()

        for index_name, weight in INDEXES.items():
            
            target_game_record = self._get_or_update_game().get_target_game(index_name)
            target_embedding = target_game_record[VALUES_NAME]

            guessed_game_record = self._database.get_similarity(index_name=index_name, name=game_name, embedding=target_embedding)
            if not guessed_game_record:
                continue

            scores.append(float(guessed_game_record[SCORE_NAME]))
            weights.append(weight)

        print("Target:", target_game_record[METADATA_NAME]["Name"], "; Guess:", game_name)

        score = self._get_weighted_similarity(similarity_scores=scores, weights=weights)
        game_comparison = self._compare_games(target_game_record[METADATA_NAME], guessed_game_record[METADATA_NAME])

        return GameGuessResponse(comparison=game_comparison, score=score)

    def get_hint(self, game_name: str) -> HintResponse:
        target_game_name = self._get_or_update_game().get_target_game(self._get_first_index_name())[METADATA_NAME]["Name"]

        hint = self._hint_generator.generate_hint(target_game_name=target_game_name, guessed_game_name=game_name)

        return HintResponse(hint=hint)

    def _get_or_update_game(self) -> DailyTargetGame:
        if not self._game or self._game.is_expired():
            self._game = self._new_game()

        return self._game

    def _new_game(self) -> DailyTargetGame:
        game_names = self._get_game_names()
        any_game_name = np.random.choice(game_names)
        
        game_records = {index_name: self._database.get_by_id(index_name=index_name, id_=any_game_name) for index_name in INDEXES}
        
        return DailyTargetGame(target_game_records=game_records)

    def _get_game_names(self) -> list[str]:
        if not self._game_names:
            self._game_names = self._database.get_ids(index_name=self._get_first_index_name())

        return self._game_names

    def _compare_games(self, base_metadata: dict, comparable_metadata: dict) -> GameComparison:
        target_game = Game.from_metadata(base_metadata)
        guessed_game = Game.from_metadata(comparable_metadata)

        return GameComparison(target_game, guessed_game)
    
    def _get_weighted_similarity(self, similarity_scores: list[float], weights: list[float]) -> float:
        return sum([score * weight for score, weight in zip(similarity_scores, weights)])
    
    def _get_first_index_name(self) -> str:
        return list(INDEXES.keys())[0]

