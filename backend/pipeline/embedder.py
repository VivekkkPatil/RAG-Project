from backend.config import EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed_texts(texts: list[str]) -> list:
    return get_model().encode(texts, show_progress_bar=False).tolist()