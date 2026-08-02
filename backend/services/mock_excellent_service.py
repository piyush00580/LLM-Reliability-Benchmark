import time
from services.llm_service import LLMService


class MockExcellentService(LLMService):

    def __init__(self):
        self.model_name = "mock_excellent"

    def generate_response(self, prompt):

        time.sleep(0.4)

        response = (
            "The provided information is factually consistent and logically coherent. "
            "It accurately summarizes the topic without introducing unsupported claims."
        )

        latency = 0.4

        return response, latency

    def get_model_name(self):
        return self.model_name