from services.benchmark_service import BenchmarkService


def test_end_to_end_benchmark_pipeline():
    service = BenchmarkService()

    result = service.run(
        text="Artificial intelligence is transforming healthcare.",
        models=["mock_excellent"],
        benchmarks=[
            "consistency",
            "hallucination",
            "information_decay",
            "prompt_robustness"
        ]
    )

    assert isinstance(result, dict)
    assert "mock_excellent" in result

    model_result = result["mock_excellent"]

    assert "benchmark_reports" in model_result
    assert "overall_reliability" in model_result

    reports = model_result["benchmark_reports"]

    assert len(reports) == 4

    benchmark_names = {
        report["benchmark"]
        for report in reports
    }

    assert benchmark_names == {
        "Consistency",
        "Hallucination",
        "Information Retention",
        "Prompt Robustness"
    }

    overall = model_result["overall_reliability"]

    assert overall is not None
    assert "overall_score" in overall
    assert "breakdown" in overall

    assert 0 <= overall["overall_score"] <= 100