from .serializable import Serializable


class GamesResponse(Serializable):
    def __init__(self, games: list[str]) -> None:
        self.games = games
