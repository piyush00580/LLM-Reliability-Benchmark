import time
from google import genai
from core.config import (
    GEMINI_API_KEY,
    DEFAULT_MODEL,
    MAX_RETRIES,
    INITIAL_RETRY_DELAY
)
from services.llm_service import LLMService

class GeminiService(LLMService):
    def __init__(self):
        self.model_name = DEFAULT_MODEL

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_response(self, prompt):
        retries = 0
        delay = INITIAL_RETRY_DELAY

        while retries <= MAX_RETRIES:
            start = time.perf_counter()

            try:
                response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
                )

                latency = time.perf_counter() - start

                return response.text, latency

            except Exception as e:
                error = str(e)

                if "429" in error and retries < MAX_RETRIES:
                    print(
                    f"\nRate limit reached. "
                    f"Retrying in {delay} seconds... "
                    f"({retries + 1}/{MAX_RETRIES})"
                   )

                    time.sleep(delay)

                    retries += 1

                    delay *= 2

                    continue

                print(f"\nGemini Error: {e}\n")

                return (
                "Generation failed due to Gemini API error.",
                time.perf_counter() - start
                )

    def get_model_name(self):
        return self.model_name