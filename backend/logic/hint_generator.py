"""Responsible for generating hints for the player to guess the targeted game."""

from ..genai.gen_ai_model import GenAIModel

DEFAULT_HINT_PROMPT = """
The player of a game has to guess the following game: {target_game_name}
The player has falsely guessed: {guessed_game_name}
Generate a hint so that the player may have a better idea of the targeted game.
You must not mention the game {target_game_name} in your response.
You must use the falsely guessed game in your hint.
You must generate a short hint with a maximum of five sentences and a minimum of one sentence.
You must not make it too easy.
"""


class HintGenerator:
    """
    Responsible for generating hints for the player to guess the targeted game.

    Attributes:
        model: The model to use for generating hints.
        hint_prompt: The prompt to use for generating hints.
    """

    def __init__(self, api_key: str, hint_prompt: str = DEFAULT_HINT_PROMPT):
        self._model = GenAIModel(api_key=api_key)
        self._hint_prompt = hint_prompt

    def generate_hint(self, target_game_name: str, guessed_game_name: str) -> str:
        """
        Generates a hint based on the names of the target game and the guessed game.

        Args:
            target_game_name (str): The name of the target game.
            guessed_game_name (str): The name of the game guessed by the player.

        Returns:
            str: The generated hint or None if the model fails to generate a hint.
        """
        try:
            prompt = self._hint_prompt.format(
                target_game_name=target_game_name, guessed_game_name=guessed_game_name
            )
            return self._model.get_response(prompt=prompt)
        except ValueError:
            return None
