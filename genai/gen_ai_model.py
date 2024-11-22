import google.generativeai as genai

# Yes, yes, very secure - should use something like: os.environ.get("GEMINI_API_KEY"))
DEFAULT_MODEL = "gemini-1.5-flash"


class GenAIModel:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self._set_api_key(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    @staticmethod
    def _set_api_key(api_key: str) -> None:
        genai.configure(api_key=api_key)

    def get_response(self, prompt: str) -> str:
        return self._model.generate_content(prompt).text
