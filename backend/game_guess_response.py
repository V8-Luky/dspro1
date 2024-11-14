class GameGuessResponse:
    def __init__(self, metadata: dict, score: float) -> None:
        self.metadata = metadata
        self.similarity = score

    def to_json(self):
        return vars(self)
