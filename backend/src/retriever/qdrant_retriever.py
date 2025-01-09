from src.stores.qdrant import DocumentStoreInstance
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from typing import Optional


class QdrantRetriever:
    _instance: Optional[QdrantEmbeddingRetriever] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = QdrantEmbeddingRetriever(
                document_store=DocumentStoreInstance.get_instance(), top_k=3
            )
        return cls._instance
