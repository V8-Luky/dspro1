import pandas as pd

from embedding.game_embedder import GameEmbedder


class GameData:
    def __init__(self, games: pd.DataFrame, embedder: GameEmbedder):
        self._games = games
        self._embedder = embedder
        _embeddings = embedder.create_game_embeddings(self._games)
        self._description_embeddings = _embeddings[0]
        self._tags_embeddings = _embeddings[1]

    @property
    def description_embedding_dimension(self):
        return int(self._description_embeddings.shape[1])

    @property
    def tags_embedding_dimension(self):
        return int(self._tags_embeddings.shape[1])

    @property
    def ids(self):
        return list(map(lambda s: ''.join(i for i in s if ord(i) < 128), map(str, self._games["Name"].tolist())))

    @property
    def description_embeddings(self):
        return self._description_embeddings

    @property
    def tags_embeddings(self):
        return self._tags_embeddings

    @property
    def metadata(self):
        return self._games.to_dict(orient="records")
