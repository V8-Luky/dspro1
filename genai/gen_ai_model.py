import google.generativeai as genai

# Yes, yes, very secure - should use something like: os.environ.get("GEMINI_API_KEY"))
API_KEY = "AIzaSyDBWwFIwzgDjSPKU0Y2I3k41b1I6RaPJ60"
DEFAULT_MODEL = "gemini-1.5-flash"


class GenAIModel:
    def __init__(self, model: str = DEFAULT_MODEL, api_key: str = API_KEY):
        self._set_api_key(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    @staticmethod
    def _set_api_key(api_key: str) -> None:
        genai.configure(api_key=api_key)

    def get_response(self, prompt: str) -> str:
        return self._model.generate_content(prompt).text
