from numpy import ndarray
from typing import Union
from sentence_transformers import SentenceTransformer
from gensim.models import KeyedVectors


class Embedder:
    def __init__(self, model: Union[SentenceTransformer, KeyedVectors]) -> None:
        self._model = model

    def create_embeddings(self, texts: list[str]) -> list[ndarray]:
        raise NotImplementedError()
