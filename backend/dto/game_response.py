from .serializable import Serializable
from logic.game import Game


class GameResponse(Serializable):
    def __init__(self, game: Game) -> None:
        self.name = game.name
        self.publishers = self._make_set_serializable(game.publishers)
        self.developers = self._make_set_serializable(game.developers)
        self.categories = self._make_set_serializable(game.categories)
        self.genres = self._make_set_serializable(game.genres)
        self.tags = self._make_set_serializable(game.tags)
        self.release_date = game.release_date.isoformat()

    def _make_set_serializable(self, set_: set) -> list:
        return list(set_)
