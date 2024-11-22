import pandas as pd


class ValidationDataset:
    def __init__(self, path: str) -> None:
        self._data = pd.read_csv(path, delimiter=';', index_col=0)

    @property
    def data(self) -> pd.DataFrame:
        """
        Returns the data as a pandas DataFrame.

        Each row contains a similarity estimation for a game, compared to another game (the column).
        The column of a game is equal to the row of the same game.

        Meanings of the values:
            0.0: The games are not similar
            0.5: The games are somewhat similar
            1.0: The games are similar
        """
        return self._data
