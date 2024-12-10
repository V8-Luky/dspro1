from numpy import ndarray
from pandas import DataFrame
from nltk.tokenize import sent_tokenize
from embedding.game_embedder import GameEmbedder
from sentence_transformers import SentenceTransformer


class DescriptionEmbedder(GameEmbedder):
    def __init__(self):
        super().__init__(SentenceTransformer("all-mpnet-base-v2"))

    def create_embeddings(self, games: DataFrame) -> ndarray:
        games['sentences'] = games["About the game"].apply(self._string_to_sentences)
        embeddings = games['sentences'].apply(lambda x: self._model.encode(x).mean(axis=0)).to_numpy()
        games.drop(columns=['sentences'], inplace=True)
        return embeddings

    def _string_to_sentences(self, text: str) -> list[str]:
        if not text:
            return ["No description available"]
        return sent_tokenize(text)
