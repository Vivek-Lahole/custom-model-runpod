from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_PORT: int = 6333
    EMBEDDING_DIM: int = 384
    INDEX_NAME: str = "snoop-dogg"
    CUSTOM_INDEX_NAME: str = "pdf-documents"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "cognitivecomputations/dolphin-2.9-llama3-8b"
    RUNPOD_API_KEY: str
    RUNPOD_ENDPOINT_ID: str

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
