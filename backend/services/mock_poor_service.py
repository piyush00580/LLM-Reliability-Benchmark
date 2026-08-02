import time
from services.llm_service import LLMService


class MockPoorService(LLMService):

    def __init__(self):
        self.model_name = "mock_poor"

    def generate_response(self, prompt):

        time.sleep(0.8)

        response = (
            "The moon is made of cheese. The Earth has two suns. "
            "Vaccines permanently change human DNA."
        )

        latency = 0.8

        return response, latency

    def get_model_name(self):
        return self.model_name