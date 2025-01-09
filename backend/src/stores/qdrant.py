from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from typing import Optional
from dotenv import load_dotenv
from ..config import get_settings

settings = get_settings()
load_dotenv()


class DocumentStoreInstance:
    _instance: Optional[QdrantDocumentStore] = None

    @classmethod
    def get_instance(
        cls,
        url: str = settings.QDRANT_URL,
        index: str = settings.INDEX_NAME,
        embedding_dim: int = settings.EMBEDDING_DIM,
        recreate_index: bool = False,
    ) -> QdrantDocumentStore:

        if cls._instance is None:
            cls._instance = QdrantDocumentStore(
                url=url,
                index=index,
                embedding_dim=embedding_dim,
                recreate_index=recreate_index,
            )
        return cls._instance
