"""Contains the DTO class for the response of a hint request."""

from .serializable import Serializable


class HintResponse(Serializable):
    """Represents the response of a hint request."""

    def __init__(self, hint: str) -> None:
        self.hint = hint
