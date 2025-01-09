from typing import List
from src.embedder.document_embedder import DocumentEmbedder
from src.stores.qdrant import DocumentStoreInstance
from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter


class PDFToDocumentPipeline:
    def __init__(self):

        self.converter = PyPDFToDocument()
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(split_by="word", split_length=50)
        self._setup_pipeline()

    def _setup_pipeline(self):
        indexing = Pipeline()
        indexing.add_component("converter", self.converter)
        indexing.add_component("cleaner", self.cleaner)
        indexing.add_component("splitter", self.splitter)

        indexing.connect("converter", "cleaner")
        indexing.connect("cleaner", "splitter")

        return indexing

    def run(self, sources: List[str]) -> List[Document]:
        result = self.pipeline.run({"converter": {"sources": sources}})
        return result["documents"]
