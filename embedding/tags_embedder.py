import numpy as np
from numpy import ndarray
from pandas import DataFrame
from embedding.embedder import Embedder


class TagsEmbedder(Embedder):
    def create_embeddings(self, games: DataFrame) -> list[ndarray]:
        game_tags = games["Tags"].apply(self._tokenize).tolist()
        embeddings = np.mean([self._model[token] for game in game_tags for token in game if token in self._model], axis=0)
        for embedding in embeddings:
            if embedding.shape[0] != 300:
                embedding = np.zeros(300)
        return embeddings

    def _tokenize(self, text: str) -> list[str]:
        return text.split(",")
