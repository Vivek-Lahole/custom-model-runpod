from haystack.components.embedders import SentenceTransformersTextEmbedder
from typing import Optional


class TextEmbedder:
    _instance: Optional[SentenceTransformersTextEmbedder] = None

    @classmethod
    def get_instance(
        cls,
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> SentenceTransformersTextEmbedder:
        if cls._instance is None:
            cls._instance = SentenceTransformersTextEmbedder(
                model=model,
            )
            cls._instance.warm_up()
        return cls._instance
