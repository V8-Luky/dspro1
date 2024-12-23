"""Contains the DTO class for the response of a game request."""

from ..logic.game import Game

from .serializable import Serializable


class GameResponse(Serializable):
    """Represents the response when requesting a single game."""

    def __init__(self, game: Game) -> None:
        self.name = game.name
        self.publishers = self._make_set_serializable(game.publishers)
        self.developers = self._make_set_serializable(game.developers)
        self.categories = self._make_set_serializable(game.categories)
        self.genres = self._make_set_serializable(game.genres)
        self.tags = self._make_set_serializable(game.tags)
        self.release_date = game.release_date.isoformat()

    def _make_set_serializable(self, set_: set) -> list:
        """Converts a set to a list, since sets are not serializable."""
        return list(set_)
