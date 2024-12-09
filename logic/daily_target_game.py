from datetime import datetime


class DailyTargetGame:
    def __init__(self, target_game_records: dict) -> None:
        self._start_time = datetime.now().date()
        self._target_game_records = target_game_records

    def get_target_game(self, key: str):
        return self._target_game_records[key]

    def is_expired(self) -> bool:
        today = datetime.now().date()
        if self._start_time.year < today.year:
            return True

        if self._start_time.month < today.month:
            return True

        return self._start_time.day < today.day
