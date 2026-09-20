import os
import requests

from services.gemini_service import GeminiService
from services.ollama_service import OllamaService
from services.groq_service import GroqService
from services.mistral_service import MistralService
from services.mock_service import MockService
from services.mock_excellent_service import MockExcellentService
from services.mock_average_service import MockAverageService
from services.mock_poor_service import MockPoorService


class LLMFactory:

    @staticmethod
    def create(model_name):

        model_name = model_name.lower()

        if model_name == "gemini":
            return GeminiService()

        elif model_name == "ollama":
            return OllamaService()

        elif model_name == "groq":
            return GroqService()

        elif model_name == "mistral":
            return MistralService()

        elif model_name == "mock":
            return MockService()

        elif model_name == "mock_excellent":
            return MockExcellentService()

        elif model_name == "mock_average":
            return MockAverageService()

        elif model_name == "mock_poor":
            return MockPoorService()

        raise ValueError(f"Unsupported model: {model_name}")

    @staticmethod
    def available_models():

        return [
            "gemini",
            "ollama",
            "groq",
            "mistral",
            "mock_excellent",
            "mock_average",
            "mock_poor"
        ]

    @staticmethod
    def create_selected(selected_models):

        return [
            LLMFactory.create(model)
            for model in selected_models
        ]

    @staticmethod
    def provider_status():

        status = {}

        status["gemini"] = {
            "name": "Google Gemini",
            "configured": bool(os.getenv("GEMINI_API_KEY")),
            "type": "cloud"
        }

        status["groq"] = {
            "name": "Groq",
            "configured": bool(os.getenv("GROQ_API_KEY")),
            "type": "cloud"
        }

        status["mistral"] = {
            "name": "Mistral",
            "configured": bool(os.getenv("MISTRAL_API_KEY")),
            "type": "cloud"
        }

        ollama_status = {
            "name": "Ollama",
            "configured": False,
            "reachable": False,
            "type": "local"
        }

        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=2
            )

            if response.ok:
                ollama_status["configured"] = True
                ollama_status["reachable"] = True

        except requests.RequestException:
            pass

        status["ollama"] = ollama_status

        return status