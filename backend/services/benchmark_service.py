from services.platform_runner import PlatformRunner
from services.llm_factory import LLMFactory
from services.plugin_manager import PluginManager
from services.benchmark_history_service import BenchmarkHistoryService


class BenchmarkService:

    def __init__(self):
        self.runner = PlatformRunner()
        self.history_service = BenchmarkHistoryService()

    def run(self, text, models, benchmarks):

        llm_services = LLMFactory.create_selected(models)

        available = {
            "consistency": None,
            "hallucination": None,
            "information_decay": None,
            "prompt_robustness": None,
        }

        for benchmark in PluginManager.discover():

            filename = benchmark.__module__.split(".")[-1]

            if filename == "consistency_benchmark":
                available["consistency"] = benchmark

            elif filename == "hallucination_benchmark":
                available["hallucination"] = benchmark

            elif filename == "information_decay_benchmark":
                available["information_decay"] = benchmark

            elif filename == "prompt_robustness_benchmark":
                available["prompt_robustness"] = benchmark

        benchmark_classes = [
            available[name]
            for name in benchmarks
            if available.get(name)
        ]

        results = self.runner.run(
            text=text,
            llm_services=llm_services,
            benchmark_classes=benchmark_classes
        )

        # Save benchmark results to SQLite
        for model, model_result in results.items():

            for report in model_result.get("benchmark_reports", []):

                score = report.get("score", 0)

                # Store scores internally as 0-1
                # even if benchmark reports return 0-100
                if score > 1:
                    score = score / 100

                latency = report.get(
                    "latency",
                    report.get("average_latency", 0)
                )

                self.history_service.save_run(
                    model=model,
                    benchmark=report["benchmark"],
                    score=score,
                    latency=latency,
                    input_text=text
                )

        return results