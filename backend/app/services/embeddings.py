"""
Embeddings service with disk cache and LRU in-memory cache.
Loads sentence-transformers model from settings.EMBEDDING_MODEL.
"""
from typing import List
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
from functools import lru_cache
from ..utils.config import load_settings
from ..utils.cache import get, put, sha256
import pickle

settings = load_settings()
MODEL_NAME = settings.EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer(MODEL_NAME)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Embedding model load failed: {e}")
    return _model

@lru_cache(maxsize=128)
def get_embedding(text: str) -> List[float]:
    key = sha256(text + MODEL_NAME)
    cached = get(key)
    if cached:
        return pickle.loads(cached)
    model = get_model()
    emb = model.encode([text])[0].tolist()
    put(key, pickle.dumps(emb))
    return emb

def embed_many(texts: List[str]) -> List[List[float]]:
    model = get_model()
    results = []
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
