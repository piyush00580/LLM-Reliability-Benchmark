from sentence_transformers.util import cos_sim
from evaluation.evaluation_metric import EvaluationMetric


class SimilarityEvaluator(EvaluationMetric):

    def evaluate(self, embedding1, embedding2):

        similarity = cos_sim(
            embedding1,
            embedding2
        )

        return {
        "score": similarity.item(),
        "unit": "cosine_similarity",
        "higher_is_better": True
    }