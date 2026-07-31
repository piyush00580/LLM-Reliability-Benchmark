import spacy

from evaluation.evaluation_metric import EvaluationMetric


class KeywordConsistencyEvaluator(EvaluationMetric):

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

    def extract_keywords(self, text):

        doc = self.nlp(text)

        keywords = {

            token.lemma_.lower()

            for token in doc

            if (
                token.pos_ in {"NOUN", "PROPN", "ADJ"}
                and not token.is_stop
                and not token.is_punct
                )
        }

        return keywords

    def evaluate(self, original_text, summary):

        original_keywords = self.extract_keywords(original_text)

        summary_keywords = self.extract_keywords(summary)

        if not summary_keywords:

            return {

                "score": 0.0,

                "matched_keywords": 0,

                "summary_keywords": 0,

                "unit": "ratio",

                "higher_is_better": True

            }

        matched = original_keywords.intersection(summary_keywords)

        score = len(matched) / len(summary_keywords)

        return {

            "score": score,

            "matched_keywords": len(matched),

            "summary_keywords": len(summary_keywords),

            "unit": "ratio",

            "higher_is_better": True

        }

        print("\nOriginal Keywords:")
        print(sorted(original_keywords))

        print("\nSummary Keywords:")
        print(sorted(summary_keywords))

        print("\nMatched Keywords:")
        print(sorted(matched))