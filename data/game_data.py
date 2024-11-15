import pandas as pd

from embedding.game_embedder import GameEmbedder


class GameData:
    def __init__(self, games: pd.DataFrame, embedder: GameEmbedder):
        self._games = games
        self._embedder = embedder
        self._embeddings = embedder.create_game_embeddings(self._games)

    @property
    def embedding_dimension(self):
        return int(self._embeddings.shape[1])

    @property
    def ids(self):
        return list(map(lambda s: ''.join(i for i in s if ord(i) < 128), map(str, self._games["name"].tolist())))

    @property
    def embeddings(self):
        return self._embeddings

    @property
    def metadata(self):
        return self._games.to_dict(orient="records")
