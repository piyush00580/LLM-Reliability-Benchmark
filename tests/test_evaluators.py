import torch

from evaluation.similarity_evaluator import SimilarityEvaluator
from evaluation.entity_consistency_evaluator import EntityConsistencyEvaluator
from evaluation.keyword_consistency_evaluator import KeywordConsistencyEvaluator


def test_similarity_identical_embeddings():
    evaluator = SimilarityEvaluator()

    embedding = torch.tensor([[1.0, 0.0, 0.0]])

    result = evaluator.evaluate(
        embedding,
        embedding
    )

    assert result["score"] == 1.0
    assert result["higher_is_better"] is True


def test_similarity_different_embeddings():
    evaluator = SimilarityEvaluator()

    embedding1 = torch.tensor([[1.0, 0.0, 0.0]])
    embedding2 = torch.tensor([[0.0, 1.0, 0.0]])

    result = evaluator.evaluate(
        embedding1,
        embedding2
    )

    assert result["score"] == 0.5


def test_entity_consistency_matching_entities():
    evaluator = EntityConsistencyEvaluator()

    original = "Virat Kohli plays cricket for India."
    summary = "Virat Kohli plays cricket for India."

    result = evaluator.evaluate(
        original,
        summary
    )

    assert result["score"] == 1.0
    assert result["matched_entities"] == result["summary_entities"]


def test_entity_consistency_empty_summary():
    evaluator = EntityConsistencyEvaluator()

    original = "Virat Kohli plays cricket for India."
    summary = "He is a famous player."

    result = evaluator.evaluate(
        original,
        summary
    )

    assert result["score"] == 1.0
    assert result["summary_entities"] == 0


def test_keyword_consistency_matching_text():
    evaluator = KeywordConsistencyEvaluator()

    original = (
        "Artificial intelligence is transforming healthcare "
        "through machine learning."
    )

    summary = (
        "Artificial intelligence is transforming healthcare "
        "through machine learning."
    )

    result = evaluator.evaluate(
        original,
        summary
    )

    assert result["score"] == 1.0
    assert result["matched_keywords"] == result["summary_keywords"]


def test_keyword_consistency_no_matching_keywords():
    evaluator = KeywordConsistencyEvaluator()

    original = (
        "Artificial intelligence improves healthcare "
        "using machine learning."
    )

    summary = (
        "Football teams compete in international tournaments."
    )

    result = evaluator.evaluate(
        original,
        summary
    )

    assert result["score"] < 1.0
    assert result["matched_keywords"] == 0