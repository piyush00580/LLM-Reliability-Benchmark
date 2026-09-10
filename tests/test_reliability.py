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