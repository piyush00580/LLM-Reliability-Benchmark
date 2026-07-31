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

        report = { "summary": summary,
                    "results": results
                }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        print("\n✓ Report exported successfully.")
        print(f"Location : {output_file}")

        return output_file