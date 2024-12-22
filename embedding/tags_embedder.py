"""This module is responsible for creating embeddings for games based on their tags."""

import gensim.downloader as api
import numpy as np
from pandas import DataFrame

from .game_embedder import GameEmbedder


class TagsEmbedder(GameEmbedder):
    """
    Represents an embedder that creates embeddings for games based on their tags.
    Uses a pre-trained word2vec model to create the embeddings.
    """

    def __init__(self):
        super().__init__(api.load('word2vec-google-news-300'))

    def create_embeddings(self, games: DataFrame) -> np.ndarray:
        game_tags = games["Tags"].apply(self._tokenize)
        embeddings = game_tags.apply(lambda x: np.mean(
            [self._model[word] for word in x if word in self._model], axis=0)).to_numpy()
        for i, embedding in enumerate(embeddings):
            if not embedding.shape or embedding.shape[0] != 300:
                embeddings[i] = np.zeros(300)
        return embeddings

    def _tokenize(self, text: str) -> list[str]:
        return text.split(",")
