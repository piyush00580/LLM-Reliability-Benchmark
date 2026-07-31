import spacy

from evaluation.evaluation_metric import EvaluationMetric


class EntityConsistencyEvaluator(EvaluationMetric):

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def evaluate(self, original_text, summary):

        original_doc = self.nlp(original_text)
        summary_doc = self.nlp(summary)

        original_entities = {
            (ent.text.lower(), ent.label_)
            for ent in original_doc.ents
        }

        summary_entities = {
            (ent.text.lower(), ent.label_)
            for ent in summary_doc.ents
        }

        if not summary_entities:
            return {
                "score": 1.0,
                "matched_entities": 0,
                "summary_entities": 0,
                "unit": "ratio",
                "higher_is_better": True
            }

        matched = original_entities.intersection(summary_entities)

        score = len(matched) / len(summary_entities)

        return {
            "score": score,
            "matched_entities": len(matched),
            "summary_entities": len(summary_entities),
            "unit": "ratio",
            "higher_is_better": True
        }