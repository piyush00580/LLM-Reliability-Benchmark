from pathlib import Path

from services.platform_runner import PlatformRunner
from services.export_service import ExportService


class DatasetRunner:

    def __init__(self):

        self.platform_runner = PlatformRunner()

    def run(self, dataset_path, llm_services):

        dataset_results = {}

        files = sorted(Path(dataset_path).rglob("*.txt"))

        if not files:
            print("\nNo dataset files found.")
            return

        print("\nRunning Dataset Benchmark...\n")

        total_files = len(files)

        for index, file in enumerate(files, start=1):

            print(
                f"[{index}/{total_files}] "
                f"Running {file.parent.name}/{file.name}"
            )

            with open(file, "r", encoding="utf-8") as f:
                text = f.read()

            dataset_results[file.name] = self.platform_runner.run(
                text=text,
                llm_services=llm_services
            )

        summary = self.generate_summary(dataset_results)

        report_path = ExportService.export_json(
            summary,
            dataset_results
        )

        self.print_summary(summary, report_path)

        return dataset_results

    def generate_summary(self, dataset_results):

        summary = {}

        for _, file_results in dataset_results.items():

            for model, result in file_results.items():

                score = result["overall_reliability"]["overall_score"]

                if model not in summary:

                    summary[model] = {
                        "total_score": 0,
                        "files": 0
                    }

                summary[model]["total_score"] += score
                summary[model]["files"] += 1

        for model in summary:

            summary[model]["average_reliability"] = round(
                summary[model]["total_score"] /
                summary[model]["files"],
                2
            )

        summary["dataset"] = {
            "total_files": len(dataset_results)
        }

        return summary

    def print_summary(self, summary, report_path):

        print("\n" + "=" * 100)
        print("DATASET BENCHMARK SUMMARY")
        print("=" * 100)

        print(f"\nFiles Evaluated : {summary['dataset']['total_files']}")

        for model, values in summary.items():

            if model == "dataset":
                continue

            print("\n" + "-" * 60)
            print(f"MODEL : {model}")
            print("-" * 60)
            print(
                f"Average Reliability : "
                f"{values['average_reliability']:.2f}/100"
            )

        print("\n" + "=" * 100)
        print(f"Report exported to : {report_path}")
        print("=" * 100)