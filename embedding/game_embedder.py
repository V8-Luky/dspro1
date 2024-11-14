from numpy import ndarray
from pandas import DataFrame

from embedding.embedder import Embedder


class GameEmbedder(Embedder):
    def create_game_embeddings(self, games: DataFrame) -> list[ndarray]:
        raise NotImplementedError()
