from .serializable import Serializable
from logic.game_comparison import GameComparison


class GameGuessResponse(Serializable):
    def __init__(self, comparison: GameComparison, score: float) -> None:
        for key, value in comparison.__dict__.items():
            setattr(self, key, value)

        self.similarity = score
