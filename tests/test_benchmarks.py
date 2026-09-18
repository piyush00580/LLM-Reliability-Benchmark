from services.llm_factory import LLMFactory

from benchmarks.consistency_benchmark import ConsistencyBenchmark
from benchmarks.hallucination_benchmark import HallucinationBenchmark
from benchmarks.information_decay_benchmark import InformationDecayBenchmark
from benchmarks.prompt_robustness_benchmark import PromptRobustnessBenchmark


TEST_TEXT = (
    "Artificial intelligence is transforming healthcare through "
    "machine learning. Hospitals use AI to analyze medical data, "
    "support diagnosis, and improve patient care."
)


def create_mock_service():
    return LLMFactory.create("mock_excellent")


def assert_common_report_structure(report):
    assert isinstance(report, dict)

    assert "benchmark" in report
    assert "model" in report
    assert "score" in report
    assert "latency" in report
    assert "total_iterations" in report
    assert "total_time" in report
    assert "metrics" in report
    assert "results" in report

    assert isinstance(report["benchmark"], str)
    assert isinstance(report["model"], str)
    assert isinstance(report["score"], (int, float))
    assert isinstance(report["latency"], (int, float))
    assert isinstance(report["total_iterations"], int)
    assert isinstance(report["total_time"], (int, float))
    assert isinstance(report["metrics"], dict)
    assert isinstance(report["results"], list)

    assert 0 <= report["score"] <= 100
    assert report["latency"] >= 0
    assert report["total_iterations"] > 0
    assert report["total_time"] >= 0
    assert len(report["results"]) > 0


def test_consistency_benchmark_contract():
    service = create_mock_service()

    benchmark = ConsistencyBenchmark(service)
    report = benchmark.run(TEST_TEXT, iterations=2)

    assert_common_report_structure(report)

    assert report["benchmark"] == "Consistency"
    assert report["model"] == "mock_excellent"
    assert report["total_iterations"] == 2
    assert len(report["results"]) == 2

    assert "SimilarityEvaluator" in report["metrics"]
    assert "CompressionEvaluator" in report["metrics"]
    assert "ReadabilityEvaluator" in report["metrics"]


def test_hallucination_benchmark_contract():
    service = create_mock_service()

    benchmark = HallucinationBenchmark(service)
    report = benchmark.run(TEST_TEXT)

    assert_common_report_structure(report)

    assert report["benchmark"] == "Hallucination"
    assert report["model"] == "mock_excellent"
    assert report["total_iterations"] == 1
    assert len(report["results"]) == 1

    assert "SimilarityEvaluator" in report["metrics"]
    assert "EntityConsistencyEvaluator" in report["metrics"]
    assert "KeywordConsistencyEvaluator" in report["metrics"]


def test_information_retention_benchmark_contract():
    service = create_mock_service()

    benchmark = InformationDecayBenchmark(service)
    report = benchmark.run(TEST_TEXT, iterations=2)

    assert_common_report_structure(report)

    assert report["benchmark"] == "Information Retention"
    assert report["model"] == "mock_excellent"
    assert report["total_iterations"] == 2

    # Includes iteration 0 baseline + requested iterations.
    assert len(report["results"]) == 3

    assert report["results"][0]["iteration"] == 0

    assert "SimilarityEvaluator" in report["metrics"]
    assert "CompressionEvaluator" in report["metrics"]
    assert "ReadabilityEvaluator" in report["metrics"]


def test_prompt_robustness_benchmark_contract():
    service = create_mock_service()

    benchmark = PromptRobustnessBenchmark(service)
    report = benchmark.run(TEST_TEXT)

    assert_common_report_structure(report)

    assert report["benchmark"] == "Prompt Robustness"
    assert report["model"] == "mock_excellent"

    assert report["total_iterations"] == len(
        PromptRobustnessBenchmark.PROMPTS
    )

    assert len(report["results"]) == len(
        PromptRobustnessBenchmark.PROMPTS
    )

    assert "SimilarityEvaluator" in report["metrics"]
    assert "CompressionEvaluator" in report["metrics"]
    assert "ReadabilityEvaluator" in report["metrics"]
    assert "PromptRobustness" in report["metrics"]


def test_consistency_result_contains_metrics():
    service = create_mock_service()

    benchmark = ConsistencyBenchmark(service)
    report = benchmark.run(TEST_TEXT, iterations=2)

    for result in report["results"]:
        assert "iteration" in result
        assert "text" in result
        assert "latency" in result
        assert "metrics" in result

        assert isinstance(result["text"], str)
        assert isinstance(result["latency"], (int, float))
        assert isinstance(result["metrics"], dict)


def test_hallucination_result_contains_metrics():
    service = create_mock_service()

    benchmark = HallucinationBenchmark(service)
    report = benchmark.run(TEST_TEXT)

    result = report["results"][0]

    assert result["iteration"] == 1
    assert isinstance(result["text"], str)
    assert isinstance(result["latency"], (int, float))
    assert isinstance(result["metrics"], dict)


def test_information_retention_baseline_result():
    service = create_mock_service()

    benchmark = InformationDecayBenchmark(service)
    report = benchmark.run(TEST_TEXT, iterations=1)

    baseline = report["results"][0]

    assert baseline["iteration"] == 0
    assert baseline["text"] == TEST_TEXT
    assert baseline["latency"] == 0.0

    assert baseline["metrics"]["SimilarityEvaluator"]["score"] == 1.0
    assert baseline["metrics"]["CompressionEvaluator"]["score"] == 0.0


def test_prompt_robustness_results_contain_prompts():
    service = create_mock_service()

    benchmark = PromptRobustnessBenchmark(service)
    report = benchmark.run(TEST_TEXT)

    for result in report["results"]:
        assert "prompt" in result
        assert isinstance(result["prompt"], str)
        assert TEST_TEXT in result["prompt"]