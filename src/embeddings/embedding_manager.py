"""
Embedding Manager Module

This module generates vector embeddings for chunked documents using Mistral AI.
It defines an EmbeddingManager class that handles the integration with Mistral's
embedding models and provides structured output via the EmbeddedDocument dataclass.
"""

import logging
import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmbeddedDocument:
    """
    Data class grouping a document chunk with its embedding and metadata.
    """
    document: Document
    embedding: List[float]
    metadata: dict


class EmbeddingManager:
    """
    Manager class for generating embeddings using Mistral AI.
    """

    def __init__(self, model_name: str = "mistral-embed"):
        """
        Initializes the Mistral embedding model.

        Args:
            model_name (str): The Mistral model to use for embeddings.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set or empty.")
            
        self.model_name = model_name
        
        # Initialize the embedding model.
        # We use `api_key` to avoid type checker errors (Unexpected keyword argument mistral_api_key)
        self._model = MistralAIEmbeddings(
            model=self.model_name,
            api_key=api_key
        )
        
        logger.info(f"EmbeddingManager initialized with model: {self.model_name}")

    def get_embedding_model(self) -> MistralAIEmbeddings:
        """
        Returns the initialized embedding model.

        Returns:
            MistralAIEmbeddings: The embedding model instance.
        """
        return self._model

    def embed_documents(self, chunks: List[Document]) -> List[EmbeddedDocument]:
        """
        Generate embeddings for a list of document chunks.

        Args:
            chunks (List[Document]): The document chunks to embed.

        Returns:
            List[EmbeddedDocument]: The chunks with their generated embeddings.
            
        Raises:
            ValueError: If the chunks list is empty or None.
        """
        if not chunks:
            raise ValueError("The chunks list provided for embedding is empty or None.")
            
        logger.info(f"Generating embeddings for {len(chunks)} chunks.")
        
        # Extract text content from documents
        texts = [chunk.page_content for chunk in chunks]
        
        # Generate embeddings in batch
        embeddings = self._model.embed_documents(texts)
        
        # Combine documents with their embeddings
        embedded_docs = []
        for chunk, embedding in zip(chunks, embeddings):
            embedded_docs.append(
                EmbeddedDocument(
                    document=chunk,
                    embedding=embedding,
                    metadata=chunk.metadata.copy() if chunk.metadata else {}
                )
            )
            
        logger.info("Successfully generated embeddings for all chunks.")
        return embedded_docs

    def embed_query(self, query: str) -> List[float]:
        """
        Generate an embedding for a single query string.

        Args:
            query (str): The query string to embed.

        Returns:
            List[float]: The generated embedding vector.
            
        Raises:
            ValueError: If the query string is empty or None.
        """
        if not query or not query.strip():
            raise ValueError("The query string is empty or None.")
            
        logger.info("Generating embedding for query.")
        return self._model.embed_query(query)

    def get_embedding_dimension(self) -> int:
        """
        Generate a sample embedding and return its dimension.

        Returns:
            int: The dimension size of the embedding vectors.
        """
        sample_query = "sample"
        sample_embedding = self.embed_query(sample_query)
        return len(sample_embedding)
