"""
Text Chunker module for the Multi-RAG system.
Responsible for splitting large LangChain Documents into semantic chunks for embedding.
"""

import logging
import uuid
from typing import List, Callable

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class KnowledgeTextChunker:
    """
    A production-ready text chunker for the Multi-RAG pipeline.
    Splits LangChain Document objects into semantic chunks suitable for embedding generation.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        length_function: Callable[[str], int] = len,
    ) -> None:
        """
        Initialize the KnowledgeTextChunker.

        Args:
            chunk_size: Maximum size of chunks to return.
            chunk_overlap: Overlap in characters between chunks.
            length_function: Function that measures the length of given chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self.length_function,
            keep_separator=True,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits a general list of Documents.

        Args:
            documents: List of LangChain Document objects.

        Returns:
            List of chunked LangChain Document objects with updated metadata.
        """
        logger.info("Chunking started (General).")
        return self._create_chunks(documents)

    def split_mmm_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits MMM domain documents.

        Args:
            documents: List of MMM LangChain Document objects.

        Returns:
            List of chunked LangChain Document objects with updated metadata.
        """
        logger.info("Chunking started (MMM).")
        return self._create_chunks(documents)

    def split_forecast_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits Forecast domain documents.

        Args:
            documents: List of Forecast LangChain Document objects.

        Returns:
            List of chunked LangChain Document objects with updated metadata.
        """
        logger.info("Chunking started (Forecast).")
        return self._create_chunks(documents)

    def split_sentiment_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits Sentiment domain documents.

        Args:
            documents: List of Sentiment LangChain Document objects.

        Returns:
            List of chunked LangChain Document objects with updated metadata.
        """
        logger.info("Chunking started (Sentiment).")
        return self._create_chunks(documents)

    def _create_chunks(self, documents: List[Document]) -> List[Document]:
        """
        Core internal logic for processing documents, applying chunking,
        and collecting statistics.

        Args:
            documents: A list of LangChain Document objects to process.

        Returns:
            A list of chunked Document objects.
        """
        if not documents:
            logger.warning("Empty document list received. Returning empty list.")
            return []

        logger.info(f"Documents received: {len(documents)}")

        final_chunks: List[Document] = []
        documents_processed = 0

        for doc in documents:
            if doc is None or not hasattr(doc, "page_content") or not hasattr(doc, "metadata"):
                logger.warning("Invalid or None document encountered. Skipping.")
                continue

            content = doc.page_content
            if not content or not content.strip():
                logger.warning("Document with empty content encountered. Skipping.")
                continue
                
            try:
                # Split the single document into raw chunks
                raw_chunks = self._splitter.split_documents([doc])
                total_chunks_for_doc = len(raw_chunks)
                
                if total_chunks_for_doc == 0:
                    continue

                # Enrich metadata for each chunk
                for idx, chunk in enumerate(raw_chunks, start=1):
                    enriched_chunk = self._update_metadata(
                        chunk=chunk,
                        chunk_index=idx,
                        total_chunks=total_chunks_for_doc
                    )
                    final_chunks.append(enriched_chunk)

                documents_processed += 1
            except Exception as e:
                logger.warning(f"Error processing document: {e}. Skipping.")
                continue

        logger.info(f"Documents processed: {documents_processed}")
        logger.info(f"Chunks created: {len(final_chunks)}")

        self._calculate_statistics(final_chunks)
        
        logger.info("Chunking completed successfully.")
        return final_chunks

    def _update_metadata(
        self, 
        chunk: Document, 
        chunk_index: int, 
        total_chunks: int
    ) -> Document:
        """
        Enhances the metadata of a chunk.

        Args:
            chunk: The LangChain Document chunk.
            chunk_index: The index of the chunk relative to its parent document (1-based).
            total_chunks: The total number of chunks produced from the parent document.

        Returns:
            The Document with updated metadata.
        """
        char_count = len(chunk.page_content)
        word_count = len(chunk.page_content.split())
        chunk_id = str(uuid.uuid4())

        chunk.metadata.update({
            "chunk_id": chunk_id,
            "chunk_index": chunk_index,
            "total_chunks": total_chunks,
            "character_count": char_count,
            "word_count": word_count,
        })
        
        return chunk

    def _calculate_statistics(self, chunks: List[Document]) -> None:
        """
        Calculates and logs statistics about the generated chunks.

        Args:
            chunks: The complete list of generated Document chunks.
        """
        if not chunks:
            logger.info("No chunks to calculate statistics for.")
            return

        sizes = [len(chunk.page_content) for chunk in chunks]
        
        avg_size = sum(sizes) / len(sizes)
        max_size = max(sizes)
        min_size = min(sizes)

        logger.info(f"Average chunk size: {avg_size:.2f} characters")
        logger.info(f"Maximum chunk size: {max_size} characters")
        logger.info(f"Minimum chunk size: {min_size} characters")
