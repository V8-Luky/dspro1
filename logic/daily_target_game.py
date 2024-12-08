from datetime import datetime


class DailyTargetGame:
    def __init__(self, target_game) -> None:
        self._start_time = datetime.now().date()
        self._target_game = target_game

    @property
    def target_game(self):
        return self._target_game

    def is_expired(self) -> bool:
        today = datetime.now().date()
        if self._start_time.year < today.year:
            return True

        if self._start_time.month < today.month:
            return True

        return self._start_time.day < today.day
