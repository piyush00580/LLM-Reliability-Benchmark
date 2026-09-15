import time

from mistralai.client import Mistral

from services.llm_service import LLMService
from core.config import MISTRAL_API_KEY


class MistralService(LLMService):

    def __init__(self):
        self.model_name = "ministral-3b-2512"

        if not MISTRAL_API_KEY:
            raise ValueError(
                "MISTRAL_API_KEY is not configured. "
                "Please add it to the .env file."
            )

        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def generate_response(self, prompt):

        start = time.perf_counter()

        try:
            response = self.client.chat.complete(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
            )

            generated_text = response.choices[0].message.content

            if not generated_text:
                raise ValueError(
                    "Mistral returned an empty response."
                )

            latency = time.perf_counter() - start

            return generated_text.strip(), latency

        except Exception as e:

            print(f"\nMistral Error: {e}\n")

            return (
                "Generation failed due to Mistral API error.",
                time.perf_counter() - start
            )

    def get_model_name(self):
        return self.model_name