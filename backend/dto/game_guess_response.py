from .serializable import Serializable


class GameGuessResponse(Serializable):
    def __init__(self, metadata: dict, score: float) -> None:
        self.metadata = metadata
        self.similarity = score
