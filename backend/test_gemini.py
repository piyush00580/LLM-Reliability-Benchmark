from google import genai
from core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Reply with only the word SUCCESS."
)

print(response.text)