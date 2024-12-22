"""Repsonsible for comparing a target game with a guessed game."""

from datetime import date

from .game import Game


class GameComparison:
    """
    Represents the comparison between a target game and a guessed game.

    Attributes:
        name: The name of the game.
        is_correct: Whether the guess was correct.
        publishers: Two sets of publishers, the matched and the unmatched publishers.
        developers: Two sets of developers, the matched and the unmatched developers.
        categories: Two sets of categories, the matched and the unmatched categories.
        genres: Two sets of genres, the matched and the unmatched genres.
        tags: Two sets of tags, the matched and the unmatched tags.
        release_date: The release date of the game, and an indicator whether 
            the guessed date is lower, equal or higher than the target date.
    """

    DATE_LOWER = -1
    DATE_EQUAL = 0
    DATE_HIGHER = 1

    def __init__(self, target_game: Game, guessed_game: Game):
        self.name = guessed_game.name
        self.is_correct = target_game.name == guessed_game.name
        self.publishers = self._compare_sets(
            target_game.publishers, guessed_game.publishers)
        self.developers = self._compare_sets(
            target_game.developers, guessed_game.developers)
        self.categories = self._compare_sets(
            target_game.categories, guessed_game.categories)
        self.genres = self._compare_sets(
            target_game.genres, guessed_game.genres)
        self.tags = self._compare_sets(target_game.tags, guessed_game.tags)
        self.release_date = self._compare_release_date(
            target_game.release_date, guessed_game.release_date)

    def _compare_release_date(self, target_date: date, guessed_date: date) -> dict[str, str]:
        result = dict()
        result["guessed"] = guessed_date.isoformat()
        result["target_direction"] = self._get_date_comparison_int(
            target_date, guessed_date)
        return result

    def _compare_sets(self, target_set: set[str], guessed_set: set[str]) -> dict[str, set[str]]:
        result = dict()
        result["match"] = guessed_set & target_set
        result["mismatch"] = guessed_set - target_set
        return result

    def _get_date_comparison_int(self, target_date: date, guessed_date: date) -> int:
        if guessed_date == target_date:
            return self.DATE_EQUAL

        if guessed_date < target_date:
            return self.DATE_LOWER

        return self.DATE_HIGHER
