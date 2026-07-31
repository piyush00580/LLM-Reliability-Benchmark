from services.gemini_service import GeminiService
from services.mock_service import MockService

class LLMFactory:

    @staticmethod
    def create(model_name):

        if model_name.lower() == "gemini":
            return GeminiService()

        elif model_name.lower() == "mock":
            return MockService()

        raise ValueError(f"Unsupported model: {model_name}")