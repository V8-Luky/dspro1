from .serializable import Serializable


class HintResponse(Serializable):
    def __init__(self, hint: str) -> None:
        self.hint = hint
