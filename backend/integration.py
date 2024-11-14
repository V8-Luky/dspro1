from database.game_database import GameDatabase
from logic.daily_game import DailyGame


class Integration:
    def __init__(self, database: GameDatabase):
        self._database = database
        self._game = self._new_game()

    def get_list(self):
        # TODO: Get list of all games
        return self._database.get_all()

    def guess(self, game_name):
        target_game = self._get_or_update_game().target_game

        # TODO: Get the data of the guessed game

        # TODO: Get the similarity between the guessed game and the target game
        result = self._database.get_similar(
            name=game_name, embedding=target_game.embedding)

        # TODO: Return result api friendly
        return result

    def _get_or_update_game(self) -> DailyGame:
        if not self._game or self._game.is_expired():
            self._game = self._new_game()

        return self._game

    def _new_game(self) -> DailyGame:
        return DailyGame(self._database.get_random())
