"""Provides a helper to provide one target game to guess per day."""

from datetime import datetime


class DailyTargetGame:
    """
    Represents a daily target game.

    Attributes:
        start_time: The time the daily game was started.
        target_game_records: The records of the target games one per type of embedding.
    """

    def __init__(self, target_game_records: dict) -> None:
        self._start_time = datetime.now().date()
        self._target_game_records = target_game_records

    def get_target_game(self, key: str):
        """
        Returns the target game record for the given key.

        Args:
            key: The key of the target game record.
        Returns:
            The target game record.
        """
        return self._target_game_records[key]

    def is_expired(self) -> bool:
        """
        Checks if the daily game is expired.

        Returns:
            True if the daily game is expired; otherwise, False.
        """

        today = datetime.now().date()
        if self._start_time.year < today.year:
            return True

        if self._start_time.month < today.month:
            return True

        return self._start_time.day < today.day
