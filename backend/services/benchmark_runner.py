from benchmarks.information_decay_benchmark import InformationDecayBenchmark
from benchmarks.prompt_robustness_benchmark import PromptRobustnessBenchmark
from benchmarks.hallucination_benchmark import HallucinationBenchmark


class BenchmarkRunner:

    def __init__(self, llm):

        self.llm = llm

        self.benchmarks = [
            InformationDecayBenchmark,
            PromptRobustnessBenchmark,
            HallucinationBenchmark
        ]

    def run_all(self, text):

        reports = []

        print("\nRunning Benchmarks...\n")

        for benchmark in self.benchmarks:

            benchmark_instance = benchmark(self.llm)

            print(f"Running {benchmark_instance.__class__.__name__}...")

            report = benchmark_instance.run(text)

            reports.append(report)

        return reports