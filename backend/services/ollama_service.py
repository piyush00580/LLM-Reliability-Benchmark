import time
import requests

from services.llm_service import LLMService


class OllamaService(LLMService):

    def __init__(self):
        self.model_name = "llama3.2:3b"
        self.url = "http://localhost:11434/api/generate"
        self.timeout = (10, 300)

    def generate_response(self, prompt):

        start = time.perf_counter()

        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "keep_alive": "5m",
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 256
                    }
                },
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            generated_text = data.get("response", "").strip()

            if not generated_text:
                raise ValueError(
                    "Ollama returned an empty response."
                )

            latency = time.perf_counter() - start

            return generated_text, latency

        except requests.exceptions.ConnectionError as e:
            print(f"\nOllama connection error: {e}\n")
            raise RuntimeError(
                "Ollama server is unavailable. "
                "Start Ollama and try again."
            ) from e

        except requests.exceptions.Timeout as e:
            print("\nOllama request timed out.\n")
            raise RuntimeError(
                "Ollama request timed out after 300 seconds."
            ) from e

        except requests.exceptions.HTTPError as e:
            print(f"\nOllama HTTP error: {e}\n")
            raise RuntimeError(
                f"Ollama returned an HTTP error: {e}"
            ) from e

        except requests.exceptions.RequestException as e:
            print(f"\nOllama request error: {e}\n")
            raise RuntimeError(
                f"Ollama request failed: {e}"
            ) from e

        except (ValueError, KeyError) as e:
            print(f"\nOllama response error: {e}\n")
            raise RuntimeError(
                f"Invalid response from Ollama: {e}"
            ) from e

        except Exception as e:
            print(f"\nUnexpected Ollama error: {e}\n")
            raise RuntimeError(
                f"Unexpected Ollama error: {e}"
            ) from e

    def get_model_name(self):
        return self.model_name