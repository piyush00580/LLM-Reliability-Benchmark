from services.platform_runner import PlatformRunner
from services.llm_factory import LLMFactory
from services.plugin_manager import PluginManager


class BenchmarkService:

    def __init__(self):
        self.runner = PlatformRunner()

    def run(self, text, models, benchmarks):

        llm_services = LLMFactory.create_selected(models)

        benchmark_classes = []

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

        return self.runner.run(
            text=text,
            llm_services=llm_services,
            benchmark_classes=benchmark_classes
        )