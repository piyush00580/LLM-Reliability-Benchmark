from services.reliability_service import ReliabilityService


def test_all_benchmarks_perfect_score():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 100},
        {"benchmark": "Hallucination", "score": 100},
        {"benchmark": "Information Retention", "score": 100},
        {"benchmark": "Prompt Robustness", "score": 100},
    ]

    result = service.compute_overall_score(reports)

    assert result["overall_score"] == 100.0


def test_weighted_reliability_score():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 80},
        {"benchmark": "Hallucination", "score": 60},
        {"benchmark": "Information Retention", "score": 90},
        {"benchmark": "Prompt Robustness", "score": 70},
    ]

    result = service.compute_overall_score(reports)

    expected = (
        80 * 0.25 +
        60 * 0.25 +
        90 * 0.25 +
        70 * 0.25
    )

    assert result["overall_score"] == round(expected, 2)


def test_empty_reports_returns_zero():
    service = ReliabilityService()

    result = service.compute_overall_score([])

    assert result["overall_score"] == 0


def test_breakdown_contains_benchmark_scores():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 85},
        {"benchmark": "Hallucination", "score": 75},
    ]

    result = service.compute_overall_score(reports)

    assert result["breakdown"]["Consistency"] == 85
    assert result["breakdown"]["Hallucination"] == 75


def test_unknown_benchmark_does_not_affect_overall_score():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 100},
        {"benchmark": "Unknown Benchmark", "score": 0},
    ]

    result = service.compute_overall_score(reports)

    assert result["overall_score"] == 100.0


def test_partial_benchmark_set():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 80},
        {"benchmark": "Hallucination", "score": 60},
    ]

    result = service.compute_overall_score(reports)

    expected = (80 * 0.25 + 60 * 0.25) / 0.50

    assert result["overall_score"] == round(expected, 2)


def test_zero_scores_return_zero():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 0},
        {"benchmark": "Hallucination", "score": 0},
        {"benchmark": "Information Retention", "score": 0},
        {"benchmark": "Prompt Robustness", "score": 0},
    ]

    result = service.compute_overall_score(reports)

    assert result["overall_score"] == 0.0


def test_mixed_extreme_scores():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 100},
        {"benchmark": "Hallucination", "score": 0},
        {"benchmark": "Information Retention", "score": 100},
        {"benchmark": "Prompt Robustness", "score": 0},
    ]

    result = service.compute_overall_score(reports)

    assert result["overall_score"] == 50.0


def test_breakdown_contains_all_known_benchmarks():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 80},
        {"benchmark": "Hallucination", "score": 70},
        {"benchmark": "Information Retention", "score": 90},
        {"benchmark": "Prompt Robustness", "score": 60},
    ]

    result = service.compute_overall_score(reports)

    assert set(result["breakdown"].keys()) == {
        "Consistency",
        "Hallucination",
        "Information Retention",
        "Prompt Robustness",
    }


def test_reliability_weights_are_returned():
    service = ReliabilityService()

    reports = [
        {"benchmark": "Consistency", "score": 80},
    ]

    result = service.compute_overall_score(reports)

    assert "weights" in result
    assert result["weights"]["Consistency"] == 0.25
    assert result["weights"]["Hallucination"] == 0.25
    assert result["weights"]["Information Retention"] == 0.25
    assert result["weights"]["Prompt Robustness"] == 0.25