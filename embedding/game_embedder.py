from typing import List

from numpy import ndarray
from pandas import DataFrame
from sentence_transformers import SentenceTransformer
import gensim.downloader as api
from embedding.description_embedder import DescriptionEmbedder
from embedding.tags_embedder import TagsEmbedder


class GameEmbedder:
    def __init__(self, description_model: str = 'all-mpnet-base-v2', tags_model: str = 'word2vec-google-news-300'):
        self._description_embedder = DescriptionEmbedder(SentenceTransformer(description_model))
        self._tags_embedder = TagsEmbedder(api.load(tags_model))

    def create_game_embeddings(self, games: DataFrame) -> list[list[ndarray]]:
        description_embeddings = self._description_embedder.create_embeddings(games)
        tags_embeddings = self._tags_embedder.create_embeddings(games)
        return [description_embeddings, tags_embeddings]
