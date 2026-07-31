from evaluation.evaluation_metric import EvaluationMetric


class CompressionEvaluator(EvaluationMetric):

    def evaluate(self, original_text, summary):

        original_words = len(original_text.split())
        summary_words = len(summary.split())

        if original_words == 0:
            compression = 0.0
        else:
            compression = (
                1 - (summary_words / original_words)
            ) * 100

        return {
            "score": round(compression, 2),
            "unit": "percentage",
            "higher_is_better": None
        }