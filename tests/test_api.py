from api import app


def get_client():
    return app.test_client()


def test_dashboard_endpoint():
    client = get_client()

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert isinstance(data, dict)


def test_history_endpoint():
    client = get_client()

    response = client.get("/api/history")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert "runs" in data
    assert "total" in data
    assert isinstance(data["runs"], list)
    assert isinstance(data["total"], int)


def test_benchmark_requires_text():
    client = get_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "",
            "models": ["mock_excellent"],
            "benchmarks": ["consistency"],
        },
    )

    assert response.status_code == 400


def test_benchmark_requires_model():
    client = get_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": [],
            "benchmarks": ["consistency"],
        },
    )

    assert response.status_code == 400


def test_benchmark_rejects_invalid_model():
    client = get_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["invalid_model"],
            "benchmarks": ["consistency"],
        },
    )

    assert response.status_code == 400


def test_benchmark_requires_benchmark():
    client = get_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent"],
            "benchmarks": [],
        },
    )

    assert response.status_code == 400


def test_benchmark_rejects_invalid_benchmark():
    client = get_client()

    response = client.post(
        "/api/benchmark",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent"],
            "benchmarks": ["invalid_benchmark"],
        },
    )

    assert response.status_code == 400


def test_compare_requires_two_models():
    client = get_client()

    response = client.post(
        "/api/compare",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent"],
            "benchmarks": ["consistency"],
        },
    )

    assert response.status_code == 400


def test_compare_rejects_invalid_model():
    client = get_client()

    response = client.post(
        "/api/compare",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent", "invalid_model"],
            "benchmarks": ["consistency"],
        },
    )

    assert response.status_code == 400


def test_compare_requires_benchmark():
    client = get_client()

    response = client.post(
        "/api/compare",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent", "mock_average"],
            "benchmarks": [],
        },
    )

    assert response.status_code == 400


def test_compare_rejects_invalid_benchmark():
    client = get_client()

    response = client.post(
        "/api/compare",
        json={
            "text": "Artificial intelligence is useful.",
            "models": ["mock_excellent", "mock_average"],
            "benchmarks": ["invalid_benchmark"],
        },
    )

    assert response.status_code == 400