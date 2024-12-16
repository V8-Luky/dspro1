"""Provides the base to create embeddings for games."""

from typing import Union

from numpy import ndarray
from pandas import DataFrame
from sentence_transformers import SentenceTransformer
from gensim.models import KeyedVectors


class GameEmbedder:
    """
    Responsible for creating embeddings for games.
    Should be considered an abstract class.

    Attributes:
        model: The model to used to create the embeddings.
    """

    def __init__(self, model: Union[SentenceTransformer, KeyedVectors]):
        self._model = model

    def create_embeddings(self, games: DataFrame) -> list[ndarray]:
        """
        Creates embeddings for the given games.

        Args:
            games: A DataFrame containing the games to create embeddings for.
        Returns:
            A list of embeddings.
        """
        raise NotImplementedError
