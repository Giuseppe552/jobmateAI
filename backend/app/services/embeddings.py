
# Lazy loading for sentence-transformers model
from __future__ import annotations
import os
from functools import lru_cache
from typing import List

_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _model = SentenceTransformer(model_name)
    return _model

@lru_cache(maxsize=2048)
def get_embedding(text: str) -> List[float]:
    model = _get_model()
    emb = model.encode([text], normalize_embeddings=True)
    return emb[0].tolist()

def embed_many(texts: List[str]) -> List[List[float]]:
    model = _get_model()
    return model.encode(texts, normalize_embeddings=True).tolist()
    for text in texts:
        key = sha256(text + MODEL_NAME)
        cached = get(key)
        if cached:
            results.append(pickle.loads(cached))
        else:
            emb = model.encode([text])[0].tolist()
            put(key, pickle.dumps(emb))
            results.append(emb)
    return results
