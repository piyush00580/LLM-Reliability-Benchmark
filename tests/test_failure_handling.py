from unittest.mock import MagicMock

from services.comparison_service import ComparisonService
from services.platform_runner import PlatformRunner


class SuccessfulBenchmark:

    def __init__(self, llm):
        self.llm = llm

    def run(self, text):
        return {
            "benchmark": "Test Benchmark",
            "model": self.llm.get_model_name(),
            "score": 80,
            "latency": 1.0,
            "metrics": {},
            "results": []
        }


class FailingBenchmark:

    def __init__(self, llm):
        self.llm = llm

    def run(self, text):
        raise RuntimeError("Benchmark execution failed")


def create_llm(name):
    llm = MagicMock()
    llm.get_model_name.return_value = name
    return llm


def test_comparison_service_preserves_successful_results():
    service = ComparisonService()

    llm = create_llm("test-model")

    reports = service.compare(
        text="Test text",
        llm_services=[llm],
        benchmark_class=SuccessfulBenchmark
    )

    assert len(reports) == 1
    assert reports[0]["model"] == "test-model"
    assert reports[0]["score"] == 80
    assert "status" not in reports[0]


def test_comparison_service_captures_benchmark_failure():
    service = ComparisonService()

    llm = create_llm("test-model")

    reports = service.compare(
        text="Test text",
        llm_services=[llm],
        benchmark_class=FailingBenchmark
    )

    assert len(reports) == 1

    report = reports[0]

    assert report["model"] == "test-model"
    assert report["status"] == "failed"
    assert report["score"] == 0
    assert "Benchmark execution failed" in report["error"]


def test_comparison_service_continues_after_one_model_fails():
    service = ComparisonService()

    failing_llm = create_llm("failing-model")
    successful_llm = create_llm("successful-model")

    class MixedBenchmark:

        def __init__(self, llm):
            self.llm = llm

        def run(self, text):
            if self.llm.get_model_name() == "failing-model":
                raise RuntimeError("Model failed")

            return {
                "benchmark": "Test Benchmark",
                "model": self.llm.get_model_name(),
                "score": 90,
                "latency": 1.0,
                "metrics": {},
                "results": []
            }

    reports = service.compare(
        text="Test text",
        llm_services=[
            failing_llm,
            successful_llm
        ],
        benchmark_class=MixedBenchmark
    )

    assert len(reports) == 2

    assert reports[0]["status"] == "failed"
    assert reports[0]["model"] == "failing-model"

    assert reports[1]["model"] == "successful-model"
    assert reports[1]["score"] == 90


def test_platform_runner_ignores_failed_benchmark_in_reliability():
    runner = PlatformRunner()

    llm = create_llm("test-model")

    successful_report = {
        "benchmark": "Consistency",
        "model": "test-model",
        "score": 80,
        "latency": 1.0,
        "metrics": {},
        "results": []
    }

    failed_report = {
        "benchmark": "Hallucination",
        "model": "test-model",
        "status": "failed",
        "error": "Provider unavailable",
        "score": 0,
        "latency": 0,
        "metrics": {},
        "results": []
    }

    runner.comparison_service.compare = MagicMock(
        return_value=[successful_report, failed_report]
    )

    results = runner.run(
        text="Test text",
        llm_services=[llm],
        benchmark_classes=[SuccessfulBenchmark]
    )

    model_result = results["test-model"]

    assert model_result["benchmark_reports"][0]["score"] == 80

    # Failed benchmark must not turn the overall score into 40.
    assert model_result["overall_reliability"]["overall_score"] == 80.0