import spacy


_nlp = None


def get_spacy_model():
    global _nlp

    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")

    return _nlp