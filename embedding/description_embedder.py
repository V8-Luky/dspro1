from numpy import ndarray
from pandas import DataFrame
from nltk.tokenize import sent_tokenize
from embedding.embedder import Embedder


class DescriptionEmbedder(Embedder):
    def create_embeddings(self, games: DataFrame) -> list[ndarray]:
        embeddings = self._model.encode(games["About the game"].apply(self._string_to_sentences)).mean(axis=0)
        assert embeddings.shape[0] == 768, f"Embedding dimension is not 768. Got {embeddings.shape[0], embeddings.shape[1]} instead."
        return embeddings

    def _string_to_sentences(self, text: str) -> list[str]:
        return sent_tokenize(text)
