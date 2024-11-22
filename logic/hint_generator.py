from genai.gen_ai_model import GenAIModel

DEFAULT_HINT_PROMPT = """
The player of a game has to guess the following game: {target_game_name}
The player has falsly guessed: {guessed_game_name}
Generate a hint so that the player may have a better idea of the targeted game.
You must not mention the name of the targeted game in your response.
You must use the falsly guessed game in your hint.
You must generate a short hint with a maximum of five sentences and a minimum uf one  sentence.
You must not make it too easy.
"""


class HintGenerator:
    def __init__(self, hint_prompt: str = DEFAULT_HINT_PROMPT):
        self._model = GenAIModel()
        self._hint_prompt = hint_prompt

    def generate_hint(self, target_game_name: str, guessed_game_name: str) -> str:
        try:
            prompt = self._hint_prompt.format(
                target_game_name=target_game_name, guessed_game_name=guessed_game_name)
            return self._model.get_response(prompt=prompt)
        except ValueError:
            return None
