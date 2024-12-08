from typing import List, Union

from numpy import ndarray
from pandas import DataFrame
from sentence_transformers import SentenceTransformer
from gensim.models import KeyedVectors


class GameEmbedder:
    def __init__(self, model: Union[SentenceTransformer, KeyedVectors]):
        self._model = model

    def create_embeddings(self, games: DataFrame) -> list[ndarray]:
        raise NotImplementedError
