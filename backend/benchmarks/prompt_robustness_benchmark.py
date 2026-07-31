import time
from itertools import combinations

from benchmarks.benchmark import Benchmark
from services.embedding_service import EmbeddingService

from evaluation.evaluation_pipeline import EvaluationPipeline
from evaluation.similarity_evaluator import SimilarityEvaluator
from evaluation.compression_evaluator import CompressionEvaluator
from evaluation.readability_evaluator import ReadabilityEvaluator


class PromptRobustnessBenchmark(Benchmark):

    PROMPTS = [

        "Summarize the following text while preserving all important information:\n\n{text}",

        "Provide a concise summary of the following text:\n\n{text}",

        "Write an executive summary of the following text:\n\n{text}",

        "Summarize the key ideas from the following passage:\n\n{text}",

        "Summarize the following text in under 150 words:\n\n{text}"

    ]

    def __init__(self, llm_service):

        self.llm = llm_service

        self.embedding = EmbeddingService()

        self.pipeline = EvaluationPipeline()

        self.pipeline.add_metric(SimilarityEvaluator())
        self.pipeline.add_metric(CompressionEvaluator())
        self.pipeline.add_metric(ReadabilityEvaluator())

    def run(self, text):

        experiment_start = time.perf_counter()

        results = []
        embeddings = []
        latencies = []

        original_embedding = self.embedding.get_embedding(text)

        for i, prompt_template in enumerate(self.PROMPTS):

            prompt = prompt_template.format(text=text)

            summary, latency = self.llm.generate_response(prompt)

            summary_embedding = self.embedding.get_embedding(summary)

            # Store embedding for pairwise comparison later
            embeddings.append(summary_embedding)

            evaluation = self.pipeline.evaluate(

                embedding1=original_embedding,
                embedding2=summary_embedding,

                original_text=text,
                summary=summary

            )

            results.append({

                "iteration": i + 1,

                "prompt": prompt,

                "text": summary,

                "latency": latency,

                "metrics": evaluation

            })

            latencies.append(latency)

        # Pairwise similarity between all summaries
        robustness_score = self.calculate_prompt_robustness(embeddings)

        metric_names = results[0]["metrics"].keys()

        metrics_summary = {}

        for metric in metric_names:

            scores = [

                result["metrics"][metric]["score"]

                for result in results

            ]

            metrics_summary[metric] = {

                "average": sum(scores) / len(scores),

                "unit": results[0]["metrics"][metric]["unit"],

                "higher_is_better":
                    results[0]["metrics"][metric]["higher_is_better"]

            }

        metrics_summary["PromptRobustness"] = {
            "average": robustness_score,
            "unit": "cosine_similarity",
            "higher_is_better": True
        }

        report = {

            "benchmark": "Prompt Robustness",

            "model": self.llm.get_model_name(),

            "total_iterations": len(self.PROMPTS),

            "total_time": time.perf_counter() - experiment_start,

            "metrics": metrics_summary,

            "primary_metric": { "name": "Prompt Robustness",
                               "score": robustness_score
                               },

            "average_latency": sum(latencies) / len(latencies),

            "results": results

        }

        return report

    def calculate_prompt_robustness(self, embeddings):

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