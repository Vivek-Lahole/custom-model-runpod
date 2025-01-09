from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from typing import Optional


class DocumentEmbedder:
    _instance: Optional[SentenceTransformersDocumentEmbedder] = None

    @classmethod
    def get_instance(
        cls,
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> SentenceTransformersDocumentEmbedder:
        if cls._instance is None:
            cls._instance = SentenceTransformersDocumentEmbedder(
                model=model,
            )
            cls._instance.warm_up()
        return cls._instance
