"""
File-based cache for embeddings and other binary data.
Key is sha256 of text (or text+model_name for embeddings).
"""
import os
import hashlib
from typing import Optional
from .config import load_settings

settings = load_settings()
CACHE_DIR = settings.CACHE_DIR
os.makedirs(CACHE_DIR, exist_ok=True)

def _get_path(key: str) -> str:
    return os.path.join(CACHE_DIR, key)

def put(key: str, value: bytes) -> None:
    """Store bytes in cache under key."""
    path = _get_path(key)
    with open(path, "wb") as f:
        f.write(value)

def get(key: str) -> Optional[bytes]:
    """Retrieve bytes from cache by key."""
    path = _get_path(key)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
