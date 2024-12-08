import pandas as pd

from embedding.game_embedder import GameEmbedder


class GameData:
    def __init__(self, games: pd.DataFrame, embedder: GameEmbedder):
        self._games = games
        self._embedder = embedder
        self._embeddings = embedder.create_embeddings(self._games)        

    @property
    def ids(self):
        return self._games["Name"].tolist()

    @property
    def embeddings(self):
        return [list(row) for row in self._embeddings]

    @property
    def metadata(self):
        return self._games.to_dict(orient="records")
