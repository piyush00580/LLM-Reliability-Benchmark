import time
from itertools import combinations

from benchmarks.benchmark import Benchmark
from evaluation.similarity_evaluator import SimilarityEvaluator
from evaluation.compression_evaluator import CompressionEvaluator
from evaluation.readability_evaluator import ReadabilityEvaluator
from evaluation.evaluation_pipeline import EvaluationPipeline
from services.embedding_service import EmbeddingService


class ConsistencyBenchmark(Benchmark):

    def __init__(self, llm_service):

        self.llm = llm_service

        self.embedding = EmbeddingService()

        self.pipeline = EvaluationPipeline()

        self.pipeline.add_metric(SimilarityEvaluator())
        self.pipeline.add_metric(CompressionEvaluator())
        self.pipeline.add_metric(ReadabilityEvaluator())

    def run(self, text, iterations=5):

        experiment_start = time.perf_counter()

        results = []
        summaries = []
        latencies = []

        metrics_summary = {}

        original_embedding = self.embedding.get_embedding(text)

        for i in range(iterations):

            prompt = ( "Summarize the following text while preserving as much "
                      "important information as possible:\n\n"
                      f"{text}"
            )

            summary, latency = self.llm.generate_response(prompt)

            summary_embedding = self.embedding.get_embedding(summary)
            evaluation = self.pipeline.evaluate(
                embedding1=original_embedding,
                embedding2=summary_embedding,
                original_text=text,
                summary=summary
            )



            results.append({
                "iteration": i + 1,
                "text": summary,
                "latency": latency,
                "metrics": evaluation
            })

            summaries.append(summary)
            latencies.append(latency)

        consistency_score = self.calculate_consistency(summaries)

        metric_names = results[0]["metrics"].keys()

        for metric in metric_names:

            scores = [
                result["metrics"][metric]["score"]
                for result in results
            ]

            metrics_summary[metric] = {
                "average": round(sum(scores) / len(scores), 4),
                "unit": results[0]["metrics"][metric]["unit"],
                "higher_is_better":
                    results[0]["metrics"][metric]["higher_is_better"]
            }

        return {
            "benchmark": "Consistency",

            "model": self.llm.get_model_name(),

            "total_iterations": iterations,

            "total_time": time.perf_counter() - experiment_start,

            "metrics": metrics_summary,

            # "consistency_score": round(consistency_score, 4),
            "primary_metric": { "name": "Consistency", 
                               "score": round(consistency_score, 4)
                               },

            "average_latency": round(
                sum(latencies) / len(latencies), 
                4
            ),

            "results": results

        }

    def calculate_consistency(self, summaries):
        if len(summaries) < 2:
            return 1.0

        embeddings = [
            self.embedding.get_embedding(summary)
            for summary in summaries
        ]

        similarity = SimilarityEvaluator()

        scores = []

        for emb1, emb2 in combinations(embeddings, 2):
            score = similarity.evaluate(
            embedding1=emb1,
            embedding2=emb2
            )["score"]

            scores.append(score)

        return sum(scores) / len(scores)