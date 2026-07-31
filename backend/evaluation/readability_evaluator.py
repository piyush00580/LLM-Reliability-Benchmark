from evaluation.evaluation_metric import EvaluationMetric
import textstat


class ReadabilityEvaluator(EvaluationMetric):

    def evaluate(self, summary):

        readability = textstat.flesch_reading_ease(summary)

        return {
            "score": round(readability, 2),
            "unit": "reading_ease",
            "higher_is_better": True
        }