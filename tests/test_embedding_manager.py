"""
Test Script for EmbeddingManager

Run:
    python tests/test_embedding_manager.py
or
    python -m tests.test_embedding_manager
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Determine the project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import core components
from src.knowledge_base.document_loader import DocumentLoader
from src.knowledge_base.text_chunker import KnowledgeTextChunker
from src.embeddings.embedding_manager import EmbeddingManager, EmbeddedDocument

# Configure logging
logging.basicConfig(level=logging.ERROR) # Minimal logging to keep output clean


def test_document_loading() -> Tuple[str, int, Dict]:
    try:
        loader = DocumentLoader(PROJECT_ROOT)
        all_docs = loader.load_all_documents()
        count = sum(len(docs) for docs in all_docs.values())
        return "PASS" if count > 0 else "FAILED", count, all_docs
    except Exception as e:
        print(f"Error in document loading: {e}")
        return "FAILED", 0, {}


def test_chunking(all_docs: Dict) -> Tuple[str, int, List]:
    try:
        chunker = KnowledgeTextChunker(chunk_size=1000, chunk_overlap=200)
        all_chunks = []
        if "mmm" in all_docs:
            all_chunks.extend(chunker.split_mmm_documents(all_docs["mmm"]))
        if "forecast" in all_docs:
            all_chunks.extend(chunker.split_forecast_documents(all_docs["forecast"]))
        if "sentiment" in all_docs:
            all_chunks.extend(chunker.split_sentiment_documents(all_docs["sentiment"]))
            
        count = len(all_chunks)
        return "PASS" if count > 0 else "FAILED", count, all_chunks
    except Exception as e:
        print(f"Error in chunk generation: {e}")
        return "FAILED", 0, []


def test_embeddings(manager: EmbeddingManager, chunks: List) -> Tuple[str, str, int, int, List[EmbeddedDocument]]:
    try:
        if not chunks:
            return "FAILED", "FAILED", 0, 0, []
            
        embedded_docs = manager.embed_documents(chunks)
        embed_count = len(embedded_docs)
        
        # Validation checks
        embed_gen_status = "PASS" if embed_count == len(chunks) and embed_count > 0 else "FAILED"
        
        dim_status = "FAILED"
        embed_dim = 0
        if embed_count > 0:
            embed_dim = len(embedded_docs[0].embedding)
            
            valid_structure = True
            all_same_dim = True
            
            for ed in embedded_docs:
                if not getattr(ed, "document", None) or not getattr(ed, "embedding", None) or getattr(ed, "metadata", None) is None:
                    valid_structure = False
                if len(ed.embedding) != embed_dim or len(ed.embedding) == 0:
                    all_same_dim = False
                    
            if valid_structure and embed_gen_status == "PASS":
                embed_gen_status = "PASS"
            else:
                embed_gen_status = "FAILED"
                
            if all_same_dim and embed_dim > 0:
                dim_status = "PASS"

        return embed_gen_status, dim_status, embed_count, embed_dim, embedded_docs
    except Exception as e:
        print(f"Error in embedding generation: {e}")
        return "FAILED", "FAILED", 0, 0, []


def test_query_embedding(manager: EmbeddingManager, query: str) -> Tuple[str, int, List[float]]:
    try:
        query_emb = manager.embed_query(query)
        dim = len(query_emb)
        status = "PASS" if dim > 0 else "FAILED"
        first_10 = query_emb[:10]
        return status, dim, first_10
    except Exception as e:
        print(f"Error in query embedding: {e}")
        return "FAILED", 0, []


def print_summary(
    docs_loaded: int,
    chunks_gen: int,
    embeds_gen: int,
    embed_dim: int,
    query_dim: int,
    query_vals: List[float],
    results: Dict[str, str]
) -> None:
    print("====================================================")
    print("EMBEDDING MANAGER VERIFICATION")
    print("====================================================")
    print(f"Documents Loaded      : {docs_loaded}")
    print(f"Chunks Generated      : {chunks_gen}")
    print(f"Embeddings Generated  : {embeds_gen}")
    print(f"Embedding Dimension   : {embed_dim if embed_dim > 0 else 'xxxx'}")
    print("====================================================")
    print("QUERY EMBEDDING")
    print(f"Dimension             : {query_dim if query_dim > 0 else 'xxxx'}")
    print("First 10 Values")
    formatted_vals = [round(v, 6) for v in query_vals]
    print(f"{formatted_vals}")
    print("====================================================")
    print("VALIDATION")
    
    keys = [
        "Document Loading", 
        "Chunk Generation", 
        "Embedding Generation", 
        "Dimension Check", 
        "Query Embedding"
    ]
    for key in keys:
        print(f"{key:<22}{results[key]}")
        
    print("\nOverall Result")
    if all(status == "PASS" for status in results.values()):
        print("SUCCESS")
    else:
        print("FAILED")
    print("====================================================")


def print_optional_preview(embedded_docs: List[EmbeddedDocument]) -> None:
    if not embedded_docs:
        return
        
    print("\n====================================================")
    print("OPTIONAL PREVIEW")
    print("====================================================")
    
    first_doc = embedded_docs[0]
    preview_text = first_doc.document.page_content[:200].replace('\n', ' ')
    
    print("Document Preview (first 200 characters):")
    print(f"{preview_text}...")
    print("\nMetadata:")
    for k, v in first_doc.metadata.items():
        print(f"  - {k}: {v}")
        
    print(f"\nEmbedding Dimension: {len(first_doc.embedding)}")
    print("First 10 embedding values:")
    formatted_vals = [round(v, 6) for v in first_doc.embedding[:10]]
    print(f"{formatted_vals}")
    print("====================================================")


def main() -> None:
    results = {
        "Document Loading": "FAILED",
        "Chunk Generation": "FAILED",
        "Embedding Generation": "FAILED",
        "Dimension Check": "FAILED",
        "Query Embedding": "FAILED"
    }

    # 1. Document Loading
    doc_status, docs_loaded, all_docs = test_document_loading()
    results["Document Loading"] = doc_status

    # 2. Chunk Generation
    chunk_status, chunks_gen, all_chunks = test_chunking(all_docs)
    results["Chunk Generation"] = chunk_status

    # Initialize Embedding Manager
    try:
        manager = EmbeddingManager()
    except Exception as e:
        print(f"Error initializing EmbeddingManager: {e}")
        manager = None

    # 3. Embeddings Generation & Dimension Check
    embeds_gen, embed_dim = 0, 0
    embedded_docs = []
    if manager and chunks_gen > 0:
        emb_status, dim_status, embeds_gen, embed_dim, embedded_docs = test_embeddings(manager, all_chunks)
        results["Embedding Generation"] = emb_status
        results["Dimension Check"] = dim_status

    # 4. Query Embedding
    query_dim = 0
    query_vals = []
    if manager:
        q_status, query_dim, query_vals = test_query_embedding(
            manager, 
            "What marketing channel generated the highest ROI?"
        )
        results["Query Embedding"] = q_status

    # Display results
    print_summary(
        docs_loaded, 
        chunks_gen, 
        embeds_gen, 
        embed_dim, 
        query_dim, 
        query_vals, 
        results
    )
    
    print_optional_preview(embedded_docs)


if __name__ == "__main__":
    main()
