from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# DEFAULT_MODEL = "gemini-flash-latest"
# DEFAULT_MODEL = "gemini-3.6-flash"
# DEFAULT_MODEL = "gemini-3.5-flash-lite"
# DEFAULT_MODEL = "gemini-3.1-flash-lite"
DEFAULT_MODEL = "gemini-2.5-flash-lite"

MAX_RETRIES = 2
INITIAL_RETRY_DELAY = 10  # seconds