"""Contains the DTO class for the response of a games request."""

from .serializable import Serializable


class GamesResponse(Serializable):
    """Represents the response when requesting all games.

    Attributes:
        games: A list of game names
    """

    def __init__(self, games: list[str]) -> None:
        self.games = games
