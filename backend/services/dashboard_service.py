import sqlite3
from pathlib import Path

from services.llm_factory import LLMFactory


class DashboardService:

    @staticmethod
    def get_stats():

        PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

        DB_PATH = (
            PROJECT_ROOT
            / "database"
            / "benchmark_history.db"
        )

        # Dataset count
        datasets_path = PROJECT_ROOT / "datasets"

        dataset_count = len(
            [
                folder
                for folder in datasets_path.iterdir()
                if folder.is_dir()
            ]
        ) if datasets_path.exists() else 0

        # Default values
        total_runs = 0
        model_count = len(LLMFactory.available_models())
        reliability = 0.0
        recent_runs = []
        chart = []

        if not DB_PATH.exists():

            return {
                "total_runs": 0,
                "models": model_count,
                "datasets": dataset_count,
                "reliability": 0.0,
                "recent_runs": [],
                "chart": []
            }

        connection = sqlite3.connect(DB_PATH)

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        # --------------------------------
        # Total benchmark runs
        # --------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM benchmark_runs
        """)

        total_runs = cursor.fetchone()["total"]

        # --------------------------------
        # Average reliability
        # --------------------------------

        cursor.execute("""
            SELECT AVG(score) AS average_score
            FROM benchmark_runs
        """)

        row = cursor.fetchone()

        if row["average_score"] is not None:

            reliability = round(
                row["average_score"] * 100,
                2
            )

        # --------------------------------
        # Recent benchmark runs
        # --------------------------------

        cursor.execute("""
            SELECT
                model,
                benchmark,
                score,
                latency,
                timestamp
            FROM benchmark_runs
            ORDER BY id DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()

        recent_runs = [

            {
                "model": row["model"],
                "benchmark": row["benchmark"],
                "score": round(row["score"] * 100, 2),
                "latency": row["latency"],
                "timestamp": row["timestamp"],
                "status": "Success"
            }

            for row in rows

        ]

        # --------------------------------
        # Reliability chart
        # --------------------------------

        cursor.execute("""
            SELECT
                benchmark,
                AVG(score) AS average_score
            FROM benchmark_runs
            GROUP BY benchmark
        """)

        rows = cursor.fetchall()

        chart = [

            {
                "name": row["benchmark"],
                "score": round(
                    row["average_score"] * 100,
                    2
                )
            }

            for row in rows

        ]

        connection.close()

        return {

            "total_runs": total_runs,

            "models": model_count,

            "datasets": dataset_count,

            "reliability": reliability,

            "recent_runs": recent_runs,

            "chart": chart

        }