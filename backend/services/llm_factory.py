from services.gemini_service import GeminiService
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