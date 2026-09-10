from api import app


def test_dashboard_endpoint():
    client = app.test_client()

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    assert response.is_json


def test_history_endpoint():
    client = app.test_client()

    response = client.get("/api/history")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert "runs" in data
    assert "total" in data


def test_benchmark_requires_text():
    client = app.test_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "",
            "models": ["mock_excellent"],
            "benchmarks": ["consistency"]
        }
    )

    assert response.status_code == 400


def test_benchmark_requires_model():
    client = app.test_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": [],
            "benchmarks": ["consistency"]
        }
    )

    assert response.status_code == 400


def test_benchmark_rejects_invalid_model():
    client = app.test_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["invalid_model"],
            "benchmarks": ["consistency"]
        }
    )

    assert response.status_code == 400


def test_benchmark_requires_benchmark():
    client = app.test_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent"],
            "benchmarks": []
        }
    )

    assert response.status_code == 400


def test_compare_requires_two_models():
    client = app.test_client()

    response = client.post(
        "/api/compare",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent"],
            "benchmarks": ["consistency"]
        }
    )

    assert response.status_code == 400