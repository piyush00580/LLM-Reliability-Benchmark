import time
from services.llm_service import LLMService


class MockService(LLMService):

    def __init__(self):
        self.model_name = "mock"

    def generate_response(self, prompt):

        time.sleep(1)

        response = (
            "This is a mock response generated for testing purposes."
        )

        latency = 1.0

        return response, latency

    def get_model_name(self):
        return self.model_name