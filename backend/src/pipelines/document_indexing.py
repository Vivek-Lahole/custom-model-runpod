from typing import List
from src.embedder.document_embedder import DocumentEmbedder
from src.stores.qdrant import DocumentStoreInstance
from haystack import Document, Pipeline
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.writers import DocumentWriter


class DocumentIndexingPipeline:
    def __init__(
        self,
    ):
        self.document_store = DocumentStoreInstance.get_instance()
        self.document_embedder = DocumentEmbedder.get_instance()
        self.writer = DocumentWriter(self.document_store, policy=DuplicatePolicy.SKIP)

    def _setup_pipeline(self):
        pipeline = Pipeline()
        pipeline.add_component("embedder", self.document_embedder)
        pipeline.add_component("writer", self.writer)

        pipeline.connect("embedder", "writer")

        return pipeline

    def run(self, documents: List[Document]):
        pipeline = self._setup_pipeline()
        result = pipeline.run({"embedder": {"documents": documents}})
        print(result)
