from backend.evaluation.keyword_consistency_evaluator import KeywordPrecisionEvaluator

evaluator = KeywordPrecisionEvaluator()

original = """
Apple released iPhone 17 in California.
"""

summary = """
Apple released iPhone 17 in California and announced a new AI assistant.
"""

print(evaluator.evaluate(original, summary))