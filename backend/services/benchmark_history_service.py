import sqlite3
from pathlib import Path
from datetime import datetime


class BenchmarkHistoryService:

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    DB_PATH = PROJECT_ROOT / "database" / "benchmark_history.db"

    def __init__(self):
        print("Database Path:", self.DB_PATH)
        self.DB_PATH.parent.mkdir(exist_ok=True)
        self.initialize_database()

    def initialize_database(self):

        connection = sqlite3.connect(self.DB_PATH)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_runs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                model TEXT,

                benchmark TEXT,

                score REAL,

                latency REAL,

                input_text TEXT

            )
        """)

        connection.commit()
        connection.close()

    def save_run(
    self,
    model,
    benchmark,
    score,
    latency,
    input_text
):
        connection = sqlite3.connect(self.DB_PATH)

        cursor = connection.cursor()

        cursor.execute(
        """
        INSERT INTO benchmark_runs
        (
            timestamp,
            model,
            benchmark,
            score,
            latency,
            input_text
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                model,
                benchmark,
                score,
                latency,
                input_text
            )
        )

        connection.commit()
        connection.close()

    def get_all_runs(self):
        connection = sqlite3.connect(self.DB_PATH)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute("""
        SELECT
            id,
            timestamp,
            model,
            benchmark,
            score,
            latency,
            input_text
        FROM benchmark_runs
        ORDER BY id DESC
    """)

        rows = cursor.fetchall()

        connection.close()

        return [dict(row) for row in rows]