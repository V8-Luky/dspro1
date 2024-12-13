from datetime import date


class Game():
    @staticmethod
    def from_metadata(metadata: dict) -> 'Game':
        return Game(
            name=metadata["Name"],
            developers=Game._convert_string_to_set(metadata["Developers"]),
            publishers=Game._convert_string_to_set(metadata["Publishers"]),
            categories=Game._convert_string_to_set(metadata["Categories"]),
            genres=Game._convert_string_to_set(metadata["Genres"]),
            tags=Game._convert_string_to_set(metadata["Tags"]),
            release_date=date.fromisoformat(metadata["Release date"])
        )

    @staticmethod
    def _convert_string_to_set(string: str) -> set[str]:
        return set(string.split(","))

    def __init__(self, name: str, developers: set[str], publishers: set[str], categories: set[str], genres: set[str], tags: set[str], release_date: date) -> None:
        self.name = name
        self.developers = developers
        self.publishers = publishers
        self.categories = categories
        self.genres = genres
        self.tags = tags
        self.release_date = release_date


