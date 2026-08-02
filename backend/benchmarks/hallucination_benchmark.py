import time

from benchmarks.benchmark import Benchmark

from services.embedding_service import EmbeddingService

from evaluation.evaluation_pipeline import EvaluationPipeline

from evaluation.similarity_evaluator import SimilarityEvaluator
from evaluation.entity_consistency_evaluator import EntityConsistencyEvaluator
from evaluation.keyword_consistency_evaluator import KeywordConsistencyEvaluator


SIMILARITY_WEIGHT = 0.50
ENTITY_WEIGHT = 0.30
KEYWORD_WEIGHT = 0.20


class HallucinationBenchmark(Benchmark):

    def __init__(self, llm_service):

        self.llm = llm_service

        self.embedding = EmbeddingService()

        self.pipeline = EvaluationPipeline()

        self.pipeline.add_metric(SimilarityEvaluator())
        self.pipeline.add_metric(EntityConsistencyEvaluator())
        self.pipeline.add_metric(KeywordConsistencyEvaluator())

    def run(self, text: str):

        experiment_start = time.perf_counter()

        prompt = (
            "Summarize the following text while preserving as much "
            "important information as possible:\n\n"
            f"{text}"
        )

        summary, latency = self.llm.generate_response(prompt)

        original_embedding = self.embedding.get_embedding(text)

        summary_embedding = self.embedding.get_embedding(summary)

        evaluation = self.pipeline.evaluate(

            embedding1=original_embedding,
            embedding2=summary_embedding,

            original_text=text,
            summary=summary

        )

        similarity_score = evaluation["SimilarityEvaluator"]["score"]

        entity_score = evaluation["EntityConsistencyEvaluator"]["score"]

        keyword_score = evaluation["KeywordConsistencyEvaluator"]["score"]

        faithfulness_score = (

            SIMILARITY_WEIGHT * similarity_score +

            ENTITY_WEIGHT * entity_score +

            KEYWORD_WEIGHT * keyword_score

        )

        metrics_summary = {}

        for metric_name, metric in evaluation.items():

            metrics_summary[metric_name] = {

                "average": metric["score"],

                "unit": metric["unit"],

                "higher_is_better": metric["higher_is_better"]

            }

        experiment_end = time.perf_counter()

        total_time = experiment_end - experiment_start

        report = {

            "benchmark": "Hallucination",

            "model": self.llm.get_model_name(),

            "total_iterations": 1,

            "total_time": total_time,

            "metrics": metrics_summary,

            "score": round(faithfulness_score * 100, 2),

            "latency": round(latency, 4),

            "results": [

                {

                    "iteration": 1,

                    "latency": latency,

                    "text": summary,

                    "metrics": evaluation

                }

            ]

        }

        return report