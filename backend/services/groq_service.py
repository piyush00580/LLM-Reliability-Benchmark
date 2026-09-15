import time

from groq import Groq

from services.llm_service import LLMService
from core.config import GROQ_API_KEY


class GroqService(LLMService):

    def __init__(self):
        self.model_name = "openai/gpt-oss-120b"

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured. "
            )

        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_response(self, prompt):

        start = time.perf_counter()

        try:
            response = self.client.chat.completions.create(
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
                raise ValueError("Groq returned an empty response.")

            latency = time.perf_counter() - start

            return generated_text.strip(), latency

        except Exception as e:

            print(f"\nGroq Error: {e}\n")

            return (
                "Generation failed due to Groq API error.",
                time.perf_counter() - start
            )

    def get_model_name(self):
        return self.model_name