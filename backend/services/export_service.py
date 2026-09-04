import csv
import json
from pathlib import Path
from datetime import datetime


class ExportService:

    REPORTS_DIR = Path("reports")

    @classmethod
    def export_json(cls, summary, results):

        cls.REPORTS_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = cls.REPORTS_DIR / f"benchmark_{timestamp}.json"

        report = {
            "summary": summary,
            "results": results
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        print("\n✓ Report exported successfully.")
        print(f"Location : {output_file}")

        return output_file

    @classmethod
    def export_csv(cls, runs):

        cls.REPORTS_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = (
            cls.REPORTS_DIR /
            f"benchmark_history_{timestamp}.csv"
        )

        fieldnames = [
            "id",
            "timestamp",
            "model",
            "benchmark",
            "score",
            "latency",
            "input_text"
        ]

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for run in runs:

                score = run.get("score", 0)

                if score <= 1:
                    score = score * 100

                writer.writerow({
                    "id": run.get("id"),
                    "timestamp": run.get("timestamp"),
                    "model": run.get("model"),
                    "benchmark": run.get("benchmark"),
                    "score": f"{score:.2f}%",
                    "latency": f"{run.get('latency', 0):.4f}s",
                    "input_text": run.get("input_text")
                })

        print("\n✓ CSV exported successfully.")
        print(f"Location : {output_file}")

        return output_file