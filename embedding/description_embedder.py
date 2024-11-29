from numpy import ndarray
from pandas import DataFrame

from embedding.game_embedder import GameEmbedder


class DescriptionEmbedder(GameEmbedder):
    def create_game_embeddings(self, games: DataFrame) -> list[ndarray]:
        return self.create_embeddings(games['About the game'].tolist())
