import time
import requests

from services.llm_service import LLMService


class OllamaService(LLMService):

    def __init__(self):
        self.model_name = "llama3.2:3b"
        self.url = "http://localhost:11434/api/generate"

    def generate_response(self, prompt):

        start = time.perf_counter()

        try:

            response = requests.post(
                self.url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            latency = time.perf_counter() - start

            return data["response"], latency

        except Exception as e:

            print(f"\nOllama Error: {e}\n")

            return (
                "Generation failed due to Ollama error.",
                time.perf_counter() - start
            )

    def get_model_name(self):
        return self.model_name