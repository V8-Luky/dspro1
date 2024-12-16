"""Contains the DTO class for the response of a game guess request."""

from logic.game_comparison import GameComparison

from .serializable import Serializable


class GameGuessResponse(Serializable):
    """Represents the response of a game guess request.

    Attributes:
        name: The name of the game.
        is_correct: Whether the guess was correct.
        publishers: Two sets of publishers, the matched and the unmatched publishers.
        developers: Two sets of developers, the matched and the unmatched developers.
        categories: Two sets of categories, the matched and the unmatched categories.
        genres: Two sets of genres, the matched and the unmatched genres.
        tags: Two sets of tags, the matched and the unmatched tags.
        release_date: The release date of the game.
        similarity: The overall similarity between the guess and the actual game.
    """

    def __init__(self, comparison: GameComparison, score: float) -> None:
        self.name = comparison.name
        self.is_correct = comparison.is_correct
        self.publishers = self._make_dict_with_sets_serializable(
            comparison.publishers)
        self.developers = self._make_dict_with_sets_serializable(
            comparison.developers)
        self.categories = self._make_dict_with_sets_serializable(
            comparison.categories)
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
        """Converts a set to a list, since sets are not serializable."""
        return list(set_)
