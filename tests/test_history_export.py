import csv
import json

from services.benchmark_history_service import BenchmarkHistoryService
from services.export_service import ExportService


def test_history_database_initializes_in_temp_directory(tmp_path):
    service = BenchmarkHistoryService()

    service.DB_PATH = tmp_path / "test_history.db"
    service.initialize_database()

    assert service.DB_PATH.exists()


def test_history_save_and_retrieve_run(tmp_path):
    service = BenchmarkHistoryService()

    service.DB_PATH = tmp_path / "test_history.db"
    service.initialize_database()

    service.save_run(
        model="mock_excellent",
        benchmark="Consistency",
        score=0.95,
        latency=1.25,
        input_text="Artificial intelligence is useful."
    )

    runs = service.get_all_runs()

    assert len(runs) == 1

    run = runs[0]

    assert run["model"] == "mock_excellent"
    assert run["benchmark"] == "Consistency"
    assert run["score"] == 0.95
    assert run["latency"] == 1.25
    assert run["input_text"] == "Artificial intelligence is useful."
    assert run["timestamp"] is not None


def test_history_stores_multiple_runs(tmp_path):
    service = BenchmarkHistoryService()

    service.DB_PATH = tmp_path / "test_history.db"
    service.initialize_database()

    service.save_run(
        model="mock_excellent",
        benchmark="Consistency",
        score=0.90,
        latency=1.0,
        input_text="First test."
    )

    service.save_run(
        model="mock_average",
        benchmark="Hallucination",
        score=0.70,
        latency=2.0,
        input_text="Second test."
    )

    runs = service.get_all_runs()

    assert len(runs) == 2

    assert runs[0]["model"] == "mock_average"
    assert runs[1]["model"] == "mock_excellent"


def test_export_json(tmp_path):
    original_reports_dir = ExportService.REPORTS_DIR
    ExportService.REPORTS_DIR = tmp_path

    try:
        summary = {
            "model": "mock_excellent",
            "score": 95
        }

        results = {
            "benchmark": "Consistency"
        }

        output_file = ExportService.export_json(
            summary,
            results
        )

        assert output_file.exists()
        assert output_file.suffix == ".json"

        with open(output_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        assert data["summary"] == summary
        assert data["results"] == results

    finally:
        ExportService.REPORTS_DIR = original_reports_dir


def test_export_csv(tmp_path):
    original_reports_dir = ExportService.REPORTS_DIR
    ExportService.REPORTS_DIR = tmp_path

    try:
        runs = [
            {
                "id": 1,
                "timestamp": "2026-09-18 12:00:00",
                "model": "mock_excellent",
                "benchmark": "Consistency",
                "score": 0.95,
                "latency": 1.2345,
                "input_text": "Test input."
            }
        ]

        output_file = ExportService.export_csv(runs)

        assert output_file.exists()
        assert output_file.suffix == ".csv"

        with open(
            output_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        assert len(rows) == 1

        row = rows[0]

        assert row["id"] == "1"
        assert row["model"] == "mock_excellent"
        assert row["benchmark"] == "Consistency"
        assert row["score"] == "95.00%"
        assert row["latency"] == "1.2345s"
        assert row["input_text"] == "Test input."

    finally:
        ExportService.REPORTS_DIR = original_reports_dir


def test_export_csv_preserves_percentage_scores(tmp_path):
    original_reports_dir = ExportService.REPORTS_DIR
    ExportService.REPORTS_DIR = tmp_path

    try:
        runs = [
            {
                "id": 1,
                "timestamp": "2026-09-18 12:00:00",
                "model": "mock_excellent",
                "benchmark": "Consistency",
                "score": 95,
                "latency": 1.0,
                "input_text": "Test input."
            }
        ]

        output_file = ExportService.export_csv(runs)

        with open(
            output_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        assert rows[0]["score"] == "95.00%"

    finally:
        ExportService.REPORTS_DIR = original_reports_dir