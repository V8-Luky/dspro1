import numpy as np
from numpy import ndarray
from pandas import DataFrame
from game_embedder import GameEmbedder
import gensim.downloader as api


class TagsEmbedder(GameEmbedder):
    def __init__(self):
        super().__init__(api.load('word2vec-google-news-300'))

    def create_embeddings(self, games: DataFrame) -> ndarray:
        game_tags = games["Tags"].apply(self._tokenize)
        embeddings = game_tags.apply(lambda x: np.mean([self._model[word] for word in x if word in self._model], axis=0)).to_numpy()
        for embedding in embeddings:
            if embedding.shape[0] != 300:
                embedding = np.zeros(300)
        return embeddings

    def _tokenize(self, text: str) -> list[str]:
        return text.split(",")
