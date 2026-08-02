from pathlib import Path

from services.llm_factory import LLMFactory


class DashboardService:

    @staticmethod
    def get_stats():

        PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
        datasets_path = PROJECT_ROOT / "datasets"

        dataset_count = len(
            [
                folder
                for folder in datasets_path.iterdir()
                if folder.is_dir()
            ]
        ) if datasets_path.exists() else 0

        model_count = len(
            LLMFactory.available_models()
            )

        return {
            "total_runs": 0,
            "models": model_count,
            "datasets": dataset_count,
            "reliability": 0
        }