import time

from benchmarks.benchmark import Benchmark
from services.embedding_service import EmbeddingService

from evaluation.evaluation_pipeline import EvaluationPipeline
from evaluation.similarity_evaluator import SimilarityEvaluator
from evaluation.compression_evaluator import CompressionEvaluator
from evaluation.readability_evaluator import ReadabilityEvaluator


class InformationDecayBenchmark(Benchmark):

    def __init__(self, llm_service):

        self.llm = llm_service

        self.embedding = EmbeddingService()

        self.pipeline = EvaluationPipeline()

        self.pipeline.add_metric(SimilarityEvaluator())
        self.pipeline.add_metric(CompressionEvaluator())
        self.pipeline.add_metric(ReadabilityEvaluator())

    def run(self, text: str, iterations: int = 5):

        experiment_start = time.perf_counter()

        results = []

        original_text = text
        current_text = text

        original_embedding = self.embedding.get_embedding(
            original_text
        )

        results.append({

            "iteration": 0,

            "metrics": {

                "SimilarityEvaluator": {
                    "score": 1.0,
                    "unit": "cosine_similarity",
                    "higher_is_better": True
                },

                "CompressionEvaluator": {
                    "score": 0.0,
                    "unit": "percentage",
                    "higher_is_better": None
                },

                "ReadabilityEvaluator": {
                    "score": 0.0,
                    "unit": "reading_ease",
                    "higher_is_better": True
                }

            },

            "latency": 0.0,

            "text": original_text

        })

        for i in range(1, iterations + 1):

            prompt = (
                "Summarize the following text while preserving as much "
                "important information as possible:\n\n"
                f"{current_text}"
            )

            summary, latency = self.llm.generate_response(prompt)

            summary_embedding = self.embedding.get_embedding(
                summary
            )

            evaluation = self.pipeline.evaluate(

                embedding1=original_embedding,
                embedding2=summary_embedding,

                original_text=original_text,
                summary=summary

            )

            results.append({

                "iteration": i,

                "metrics": evaluation,

                "latency": latency,

                "text": summary

            })

            current_text = summary

        experiment_end = time.perf_counter()

        total_time = experiment_end - experiment_start

        benchmark_results = results[1:]

        average_metrics = {}

        first_result = benchmark_results[0]["metrics"]

        for metric_name in first_result:

            total = sum(

                result["metrics"][metric_name]["score"]

                for result in benchmark_results

            )

            average_metrics[metric_name] = {

                "average": total / len(benchmark_results),

                "unit":
                    first_result[metric_name]["unit"],

                "higher_is_better":
                    first_result[metric_name]["higher_is_better"]

            }

        latencies = [

            result["latency"]

            for result in benchmark_results

        ]

        average_latency = sum(latencies) / len(latencies)

        report = {

            "benchmark": "Information Decay",

            "model": self.llm.get_model_name(),

            "total_iterations": iterations,

            "total_time": total_time,

            "metrics": average_metrics,

            "score": round(
                            average_metrics["SimilarityEvaluator"]["average"] * 100,
                            2
            ),

            "latency": round(average_latency, 4),

            "results": results

        }

        return report