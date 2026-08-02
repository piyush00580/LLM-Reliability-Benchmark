import time
from services.llm_service import LLMService


class MockAverageService(LLMService):

    def __init__(self):
        self.model_name = "mock_average"

    def generate_response(self, prompt):

        time.sleep(0.6)

        response = (
            "The information appears mostly correct, although a few details are vague "
            "and some statements could be interpreted differently."
        )

        latency = 0.6

        return response, latency

    def get_model_name(self):
        return self.model_name