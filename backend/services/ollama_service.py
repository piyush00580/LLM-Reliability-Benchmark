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

            generated_text = data.get("response", "").strip()

            if not generated_text:
                raise ValueError("Ollama returned an empty response.")

            latency = time.perf_counter() - start

            return generated_text, latency

        except requests.exceptions.ConnectionError:
            print("\nOllama Error: Server is not running.\n")

            return (
                "Generation failed: Ollama server is unavailable.",
                time.perf_counter() - start
            )

        except requests.exceptions.Timeout:
            print("\nOllama Error: Request timed out.\n")

            return (
                "Generation failed: Ollama request timed out.",
                time.perf_counter() - start
            )

        except requests.exceptions.HTTPError as e:
            print(f"\nOllama HTTP Error: {e}\n")

            return (
                "Generation failed: Ollama returned an HTTP error.",
                time.perf_counter() - start
            )

        except (ValueError, KeyError) as e:
            print(f"\nOllama Response Error: {e}\n")

            return (
                "Generation failed: Invalid response from Ollama.",
                time.perf_counter() - start
            )

        except requests.exceptions.RequestException as e:
            print(f"\nOllama Request Error: {e}\n")

            return (
                "Generation failed: Ollama request error.",
                time.perf_counter() - start
            )

        except Exception as e:
            print(f"\nUnexpected Ollama Error: {e}\n")

            return (
                "Generation failed due to an unexpected Ollama error.",
                time.perf_counter() - start
            )

    def get_model_name(self):
        return self.model_name