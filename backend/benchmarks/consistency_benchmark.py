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

    def run(self, text, iterations=2):

        experiment_start = time.perf_counter()

        results = []
        summaries = []
        summary_embeddings = []
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
            summary_embeddings.append(summary_embedding)
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

        consistency_score = self.calculate_consistency(
            summary_embeddings
        )

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

            "score": round(consistency_score * 100, 2),

            "latency": round(sum(latencies) / len(latencies), 4),

            "total_iterations": iterations,

            "total_time": time.perf_counter() - experiment_start,

            "metrics": metrics_summary,

            "results": results
    }

    def calculate_consistency(self, embeddings):
        if len(embeddings) < 2:
            return 1.0

        similarity = SimilarityEvaluator()

        scores = []

        for emb1, emb2 in combinations(embeddings, 2):

                score = similarity.evaluate(
                    embedding1=emb1,
                    embedding2=emb2
                )["score"]

                scores.append(score)

        if not scores:
            return 0.0

        return sum(scores) / len(scores)