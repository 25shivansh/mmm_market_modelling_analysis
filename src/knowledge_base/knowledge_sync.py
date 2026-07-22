"""
KnowledgeSync orchestrates the knowledge ingestion workflow from MongoDB to Pinecone.
"""

from src.embeddings.embedding_manager import EmbeddingManager
from src.knowledge_base.mongo_document_loader import MongoDocumentLoader
from src.knowledge_base.text_chunker import KnowledgeTextChunker
from src.vectorstore.pinecone_manager import PineconeManager


class KnowledgeSync:
    """Orchestrator for loading, chunking, embedding, and storing report documents."""

    def __init__(self, loader=None, chunker=None, embedding_manager=None, pinecone_manager=None):
        self.loader = loader or MongoDocumentLoader()
        self.chunker = chunker or KnowledgeTextChunker()
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self.pinecone_manager = pinecone_manager or PineconeManager()

    def _validate_string(self, value, param_name):
        """Validate that value is a non-empty string."""
        if not isinstance(value, str):
            raise ValueError(f"{param_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{param_name} cannot be empty.")
        return value.strip()

    def _sync_documents(self, documents):
        """Internal helper to process documents through chunking, embedding, and vector upload."""
        if not documents:
            return 0
        chunks = self.chunker.split_documents(documents)
        if not chunks:
            return 0
        embedded_docs = self.embedding_manager.embed_documents(chunks)
        return self.pinecone_manager.upsert_documents(embedded_docs)

    def sync_all_reports(self):
        """Synchronize all reports from MongoDB to Pinecone."""
        documents = self.loader.load_all_documents()
        return self._sync_documents(documents)

    def sync_category(self, category):
        """Synchronize reports of a specific category from MongoDB to Pinecone."""
        category = self._validate_string(category, "category")
        documents = self.loader.load_documents_by_category(category)
        return self._sync_documents(documents)

    def sync_report(self, report_id):
        """Synchronize a single report by ID from MongoDB to Pinecone."""
        report_id = self._validate_string(report_id, "report_id")
        doc = self.loader.load_document(report_id)
        if not doc:
            return 0
        return self._sync_documents([doc])

    def count_reports(self):
        """Return the total number of reports stored in MongoDB."""
        return self.loader.count_documents()

    def count_chunks(self, documents):
        """Count the total number of chunks generated from a list of documents."""
        if documents is None or not isinstance(documents, list):
            raise ValueError("documents must be a list.")
        chunks = self.chunker.split_documents(documents)
        return len(chunks)
