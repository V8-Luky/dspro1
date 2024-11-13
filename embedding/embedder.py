from numpy import ndarray

from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, transformer: SentenceTransformer = None, transformer_name: str = "all-MiniLM-L6-v2") -> None:
        if not transformer:
            transformer = SentenceTransformer(transformer_name)
        self._transformer = transformer

    def create_embeddings(self, texts: list[str]) -> list[ndarray]:
        return self._transformer.encode(texts)
