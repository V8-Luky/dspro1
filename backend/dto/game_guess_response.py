from .serializable import Serializable
from logic.game_comparison import GameComparison


class GameGuessResponse(Serializable):
    def __init__(self, comparison: GameComparison, score: float) -> None:
        self.name = comparison.name
        self.is_correct = comparison.is_correct
        self.publishers = self._make_dict_with_sets_serializable(comparison.publishers)
        self.developers = self._make_dict_with_sets_serializable(comparison.developers)
        self.categories = self._make_dict_with_sets_serializable(comparison.categories)
        self.genres = self._make_dict_with_sets_serializable(comparison.genres)
        self.tags = self._make_dict_with_sets_serializable(comparison.tags)
        self.release_date = comparison.release_date

        self.similarity = score

    def _make_dict_with_sets_serializable(self, dict_: dict) -> dict:
        for key, value in dict_.items():
            if isinstance(value, set):
                dict_[key] = self._make_set_serializable(value)
        return dict_

    def _make_set_serializable(self, set_: set) -> list:
        return list(set_)
