import pandas as pd

from embedding.game_embedder import GameEmbedder


class GameData:
    def __init__(self, games, embedder: GameEmbedder):
        self._games = games
        self._embedder = embedder
        self._embeddings = self._embedder.create_embeddings(self._games)

    @property
    def ids(self) -> list[str]:
        return self._games["Name"].tolist()

    @property
    def embeddings(self) -> list[list[float]]:
        return [list(row) for row in self._embeddings]

    @property
    def metadata(self) -> list[dict]:
        games = self._games.drop(columns=["About the game","Positive", "Negative", "Estimated owners"])
        return games.to_dict(orient="records")
