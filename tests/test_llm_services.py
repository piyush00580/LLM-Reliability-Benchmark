from unittest.mock import MagicMock, patch

from services.gemini_service import GeminiService
from services.groq_service import GroqService
from services.mistral_service import MistralService
from services.ollama_service import OllamaService


# ─────────────────────────────────────────────
# Gemini
# ─────────────────────────────────────────────

@patch("services.gemini_service.genai.Client")
def test_gemini_success(mock_client):
    mock_response = MagicMock()
    mock_response.text = "Generated Gemini response"

    mock_client.return_value.models.generate_content.return_value = mock_response

    service = GeminiService()

    text, latency = service.generate_response("Test prompt")

    assert text == "Generated Gemini response"
    assert latency >= 0

    mock_client.return_value.models.generate_content.assert_called_once_with(
        model=service.model_name,
        contents="Test prompt"
    )


@patch("services.gemini_service.genai.Client")
def test_gemini_api_error(mock_client):
    mock_client.return_value.models.generate_content.side_effect = Exception(
        "Gemini API error"
    )

    service = GeminiService()

    text, latency = service.generate_response("Test prompt")

    assert "Generation failed" in text
    assert latency >= 0


# ─────────────────────────────────────────────
# Groq
# ─────────────────────────────────────────────

@patch("services.groq_service.Groq")
def test_groq_success(mock_groq):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Generated Groq response"

    mock_groq.return_value.chat.completions.create.return_value = mock_response

    service = GroqService()

    text, latency = service.generate_response("Test prompt")

    assert text == "Generated Groq response"
    assert latency >= 0

    mock_groq.return_value.chat.completions.create.assert_called_once_with(
        model=service.model_name,
        messages=[
            {
                "role": "user",
                "content": "Test prompt"
            }
        ],
        temperature=0.2,
    )


@patch("services.groq_service.Groq")
def test_groq_api_error(mock_groq):
    mock_groq.return_value.chat.completions.create.side_effect = Exception(
        "Groq API error"
    )

    service = GroqService()

    text, latency = service.generate_response("Test prompt")

    assert "Generation failed" in text
    assert latency >= 0


# ─────────────────────────────────────────────
# Mistral
# ─────────────────────────────────────────────

@patch("services.mistral_service.Mistral")
def test_mistral_success(mock_mistral):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Generated Mistral response"

    mock_mistral.return_value.chat.complete.return_value = mock_response

    service = MistralService()

    text, latency = service.generate_response("Test prompt")

    assert text == "Generated Mistral response"
    assert latency >= 0

    mock_mistral.return_value.chat.complete.assert_called_once_with(
        model=service.model_name,
        messages=[
            {
                "role": "user",
                "content": "Test prompt"
            }
        ],
        temperature=0.2,
    )


@patch("services.mistral_service.Mistral")
def test_mistral_api_error(mock_mistral):
    mock_mistral.return_value.chat.complete.side_effect = Exception(
        "Mistral API error"
    )

    service = MistralService()

    text, latency = service.generate_response("Test prompt")

    assert "Generation failed" in text
    assert latency >= 0


# ─────────────────────────────────────────────
# Ollama
# ─────────────────────────────────────────────

@patch("services.ollama_service.requests.post")
def test_ollama_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": "Generated Ollama response"
    }

    mock_post.return_value = mock_response

    service = OllamaService()

    text, latency = service.generate_response("Test prompt")

    assert text == "Generated Ollama response"
    assert latency >= 0

    mock_post.assert_called_once_with(
        service.url,
        json={
            "model": service.model_name,
            "prompt": "Test prompt",
            "stream": False
        },
        timeout=120
    )


@patch("services.ollama_service.requests.post")
def test_ollama_connection_error(mock_post):
    import requests

    mock_post.side_effect = requests.exceptions.ConnectionError()

    service = OllamaService()

    text, latency = service.generate_response("Test prompt")

    assert "server is unavailable" in text.lower()
    assert latency >= 0