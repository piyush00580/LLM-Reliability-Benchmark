from sentence_transformers.util import cos_sim
from evaluation.evaluation_metric import EvaluationMetric


class SimilarityEvaluator(EvaluationMetric):

    def evaluate(self, embedding1, embedding2):

        similarity = cos_sim(
            embedding1,
            embedding2
        ).item()

        # Convert cosine similarity from [-1, 1] to [0, 1]
        normalized_similarity = (similarity + 1) / 2

        return {
            "score": normalized_similarity,
            "unit": "cosine_similarity",
            "higher_is_better": True
        }