"""
AppSettings using pydantic-settings for FastAPI config.
Singleton loader for settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional

class AppSettings(BaseSettings):
    DEBUG: bool = False
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CACHE_DIR: str = ".cache"
    RATE_LIMIT_PER_MIN: int = 10

_settings: Optional[AppSettings] = None

def load_settings() -> AppSettings:
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings
