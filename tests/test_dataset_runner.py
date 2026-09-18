from unittest.mock import MagicMock, patch

from services.dataset_runner import DatasetRunner


def create_dataset(tmp_path):
    dataset_dir = tmp_path / "dataset"

    finance_dir = dataset_dir / "finance"
    healthcare_dir = dataset_dir / "healthcare"

    finance_dir.mkdir(parents=True)
    healthcare_dir.mkdir(parents=True)

    (finance_dir / "finance_01.txt").write_text(
        "The stock market experienced moderate growth.",
        encoding="utf-8"
    )

    (healthcare_dir / "healthcare_01.txt").write_text(
        "Regular exercise supports cardiovascular health.",
        encoding="utf-8"
    )

    return dataset_dir


def mock_platform_result(model_name, score):
    return {
        model_name: {
            "benchmark_reports": [],
            "overall_reliability": {
                "overall_score": score,
                "breakdown": {},
                "weights": {}
            }
        }
    }


def test_generate_summary():
    runner = DatasetRunner()

    dataset_results = {
        "finance_01.txt": mock_platform_result("test-model", 80),
        "healthcare_01.txt": mock_platform_result("test-model", 60),
    }

    summary = runner.generate_summary(dataset_results)

    assert summary["test-model"]["files"] == 2
    assert summary["test-model"]["total_score"] == 140
    assert summary["test-model"]["average_reliability"] == 70.0
    assert summary["dataset"]["total_files"] == 2


def test_generate_summary_multiple_models():
    runner = DatasetRunner()

    dataset_results = {
        "finance_01.txt": {
            "model-a": {
                "overall_reliability": {
                    "overall_score": 80
                }
            },
            "model-b": {
                "overall_reliability": {
                    "overall_score": 60
                }
            }
        },
        "healthcare_01.txt": {
            "model-a": {
                "overall_reliability": {
                    "overall_score": 100
                }
            },
            "model-b": {
                "overall_reliability": {
                    "overall_score": 40
                }
            }
        }
    }

    summary = runner.generate_summary(dataset_results)

    assert summary["model-a"]["files"] == 2
    assert summary["model-a"]["average_reliability"] == 90.0

    assert summary["model-b"]["files"] == 2
    assert summary["model-b"]["average_reliability"] == 50.0

    assert summary["dataset"]["total_files"] == 2


def test_generate_summary_empty_dataset():
    runner = DatasetRunner()

    summary = runner.generate_summary({})

    assert summary["dataset"]["total_files"] == 0


def test_run_dataset(tmp_path):
    runner = DatasetRunner()
    dataset_dir = create_dataset(tmp_path)

    mock_llm = MagicMock()
    mock_llm.get_model_name.return_value = "test-model"

    platform_result = mock_platform_result("test-model", 85)

    with patch.object(
        runner.platform_runner,
        "run",
        return_value=platform_result
    ) as mock_run, patch(
        "services.dataset_runner.ExportService.export_json",
        return_value="reports/test_dataset.json"
    ) as mock_export:

        results = runner.run(
            dataset_path=dataset_dir,
            llm_services=[mock_llm]
        )

    assert results is not None
    assert len(results) == 2
    assert "finance_01.txt" in results
    assert "healthcare_01.txt" in results

    assert mock_run.call_count == 2
    assert mock_export.call_count == 1


def test_run_empty_dataset(tmp_path):
    runner = DatasetRunner()

    empty_dataset = tmp_path / "empty_dataset"
    empty_dataset.mkdir()

    mock_llm = MagicMock()

    results = runner.run(
        dataset_path=empty_dataset,
        llm_services=[mock_llm]
    )

    assert results is None