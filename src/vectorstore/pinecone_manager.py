"""
Pinecone Manager Module

Responsible for storing embedded documents in a Pinecone vector database.
"""

import logging
import os
import uuid
from typing import List, Dict, Any

from dotenv import load_dotenv
from pinecone import Pinecone

from src.embeddings.embedding_manager import EmbeddedDocument

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PineconeManager:
    """
    Manager class for Pinecone vector database interactions.
    """

    def __init__(self):
        """
        Initializes the Pinecone client and connects to the marketing-rag index.
        """
        load_dotenv()
        api_key = os.getenv("PINECONE_API_KEY")
        
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set or empty.")
            
        self.index_name = "marketing-rag"
        
        try:
            # Initialize Pinecone client using the new SDK
            self.pc = Pinecone(api_key=api_key)
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client: {e}")
            raise RuntimeError(f"Could not connect to Pinecone: {e}")

    def get_index(self):
        """
        Return the connected Pinecone index.
        
        Returns:
            The Pinecone index object.
        """
        return self.index

    def upsert_documents(self, embedded_documents: List[EmbeddedDocument], batch_size: int = 100) -> int:
        """
        Store a list of embedded documents in the Pinecone index using batch uploads.
        
        Args:
            embedded_documents (List[EmbeddedDocument]): The documents to upsert.
            batch_size (int, optional): Number of vectors per batch. Defaults to 100.
            
        Returns:
            int: Number of successfully uploaded vectors.
            
        Raises:
            ValueError: If the input list is empty, or if an embedded document 
                        is missing required fields (embedding or document).
            RuntimeError: If a batch fails during the Pinecone upsert.
        """
        if not embedded_documents:
            raise ValueError("The embedded_documents list is empty.")
            
        logger.info("Upload started")
        vectors_to_upsert = []
        
        for ed in embedded_documents:
            if not ed.document:
                raise ValueError("An EmbeddedDocument is missing its 'document' attribute.")
            if not ed.embedding:
                raise ValueError("An EmbeddedDocument is missing its 'embedding' attribute.")
            if ed.metadata is None:
                raise ValueError("An EmbeddedDocument is missing its 'metadata' attribute.")
                
            # Copy metadata and add the original text
            meta = ed.metadata.copy()
            meta["text"] = ed.document.page_content
            
            # Determine vector ID (use chunk_id from metadata if present, else generate one)
            vec_id = meta.get("chunk_id")
            if not vec_id:
                vec_id = str(uuid.uuid4())
                meta["chunk_id"] = vec_id
                
            # Create vector payload
            vector = {
                "id": str(vec_id),
                "values": ed.embedding,
                "metadata": meta
            }
            vectors_to_upsert.append(vector)
            
        total_vectors = len(vectors_to_upsert)
        total_batches = (total_vectors + batch_size - 1) // batch_size
        uploaded_count = 0
        
        for i in range(total_batches):
            batch_num = i + 1
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, total_vectors)
            batch = vectors_to_upsert[start_idx:end_idx]
            
            logger.info(f"Uploading batch {batch_num}/{total_batches} ({len(batch)} vectors)")
            try:
                response = self.index.upsert(vectors=batch)
                uploaded_count += response.get('upserted_count', 0)
            except Exception as e:
                logger.error(f"Batch {batch_num} failed: {e}")
                raise RuntimeError(f"Batch {batch_num} failed during Pinecone upsert: {e}")

        logger.info("Upload completed successfully")
        logger.info(f"Total uploaded vectors: {uploaded_count}")
        return uploaded_count

    def describe_index(self) -> Dict[str, Any]:
        """
        Return useful index information.
        
        Returns:
            Dict containing index name, total vectors, and dimension.
        """
        try:
            # We can get dimension from describe_index and vector count from index stats
            info = self.pc.describe_index(self.index_name)
            stats = self.index.describe_index_stats()
            
            return {
                "index_name": self.index_name,
                "dimension": info.dimension,
                "total_vectors": stats.total_vector_count,
                "host": info.host
            }
        except Exception as e:
            logger.error(f"Failed to describe index: {e}")
            raise RuntimeError(f"Error describing index: {e}")

    def delete_all_vectors(self) -> None:
        """
        Delete every vector from the index.
        """
        try:
            logger.info(f"Deleting all vectors from index: {self.index_name}")
            self.index.delete(delete_all=True)
            logger.info("Delete completed.")
        except Exception as e:
            logger.error(f"Failed to delete all vectors: {e}")
            raise RuntimeError(f"Error during vector deletion: {e}")

    def get_index_stats(self) -> Dict[str, Any]:
        """
        Return Pinecone index statistics.
        
        Returns:
            Dict containing detailed index statistics.
        """
        try:
            stats = self.index.describe_index_stats()
            # Pinecone stats object has a to_dict method
            return stats.to_dict() if hasattr(stats, "to_dict") else dict(stats)
        except Exception as e:
            logger.error(f"Failed to fetch index statistics: {e}")
            raise RuntimeError(f"Error fetching index stats: {e}")
