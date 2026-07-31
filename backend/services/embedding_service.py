from sentence_transformers import SentenceTransformer


class EmbeddingService:

    _model = None
    _cache = {}

    def __init__(self):

        if EmbeddingService._model is None:
            from utils.logger import get_logger
            logger = get_logger(__name__)
            logger.info("Loading embedding model...")
            EmbeddingService._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

    def get_embedding(self, text):

        if text in EmbeddingService._cache:
            return EmbeddingService._cache[text]

        embedding = EmbeddingService._model.encode(
            text,
            convert_to_tensor=True
        )

        EmbeddingService._cache[text] = embedding

        return embedding