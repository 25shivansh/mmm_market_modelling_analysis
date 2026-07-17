"""
Test Script for PineconeManager

Run:
    python tests/test_pinecone_manager.py
or
    python -m tests.test_pinecone_manager
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Determine the project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import core components
from src.knowledge_base.document_loader import DocumentLoader
from src.knowledge_base.text_chunker import KnowledgeTextChunker
from src.embeddings.embedding_manager import EmbeddingManager, EmbeddedDocument
from src.vectorstore.pinecone_manager import PineconeManager

# Configure logging
logging.basicConfig(level=logging.ERROR) # Minimal logging to keep output clean


def print_header() -> None:
    print("====================================================")
    print("PINECONE MANAGER VERIFICATION")
    print("====================================================")


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


def test_embeddings(chunks: List) -> Tuple[str, int, List[EmbeddedDocument]]:
    try:
        if not chunks:
            return "FAILED", 0, []
        manager = EmbeddingManager()
        embedded_docs = manager.embed_documents(chunks)
        count = len(embedded_docs)
        status = "PASS" if count == len(chunks) and count > 0 else "FAILED"
        return status, count, embedded_docs
    except Exception as e:
        print(f"Error in embedding generation: {e}")
        return "FAILED", 0, []


def test_pinecone_upload(embedded_docs: List[EmbeddedDocument]) -> Tuple[str, str, str, int, Dict[str, Any], Any]:
    conn_status = "FAILED"
    upload_status = "FAILED"
    stats_status = "FAILED"
    uploaded_count = 0
    index_stats = {}
    manager = None
    
    try:
        manager = PineconeManager()
        conn_status = "PASS"
    except Exception as e:
        print(f"Error initializing PineconeManager: {e}")
        return conn_status, upload_status, stats_status, uploaded_count, index_stats, manager

    try:
        if embedded_docs:
            uploaded_count = manager.upsert_documents(embedded_docs)
            if uploaded_count == len(embedded_docs):
                upload_status = "PASS"
    except Exception as e:
        print(f"Error in vector upload: {e}")

    try:
        if manager:
            index_stats = manager.describe_index()
            if index_stats and "total_vectors" in index_stats:
                stats_status = "PASS"
    except Exception as e:
        print(f"Error retrieving index stats: {e}")

    return conn_status, upload_status, stats_status, uploaded_count, index_stats, manager


def print_summary(
    docs_loaded: int,
    chunks_gen: int,
    embeds_gen: int,
    vectors_up: int,
    index_stats: Dict[str, Any],
    results: Dict[str, str]
) -> None:
    print_header()
    print(f"Documents Loaded      : {docs_loaded}")
    print(f"Chunks Generated      : {chunks_gen}")
    print(f"Embeddings Generated  : {embeds_gen}")
    print(f"Vectors Uploaded      : {vectors_up}")
    print("====================================================")
    
    print("INDEX INFORMATION")
    print(f"Index Name            : {index_stats.get('index_name', 'marketing-rag')}")
    print(f"Total Vector Count    : {index_stats.get('total_vectors', 'xxxx')}")
    print(f"Dimension             : {index_stats.get('dimension', 'xxxx')}")
    print("====================================================")
    
    print("VALIDATION")
    keys = [
        "Pinecone Connection",
        "Document Loading", 
        "Chunk Generation", 
        "Embedding Generation", 
        "Vector Upload",
        "Index Statistics"
    ]
    
    for key in keys:
        status = results.get(key, "FAILED")
        colored_status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if status == "PASS" else f"{Fore.RED}FAILED{Style.RESET_ALL}"
        print(f"{key:<22} {colored_status}")
        
    print("\nOverall Result")
    if all(status == "PASS" for status in results.values()):
        print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}FAILED{Style.RESET_ALL}")
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
    print("====================================================")


def cleanup_prompt(manager: PineconeManager) -> None:
    if not manager:
        return
    print("\n====================================================")
    print("OPTIONAL CLEANUP")
    print("====================================================")
    try:
        user_input = input("Delete uploaded vectors? (y/n): ").strip().lower()
        if user_input == 'y':
            manager.delete_all_vectors()
            print("Cleanup completed.")
        else:
            print("Vectors kept in Pinecone.")
    except EOFError:
        print("Vectors kept in Pinecone (no input available).")
    except Exception as e:
        print(f"Cleanup skipped or failed: {e}")
    print("====================================================")


def main() -> None:
    results = {
        "Pinecone Connection": "FAILED",
        "Document Loading": "FAILED",
        "Chunk Generation": "FAILED",
        "Embedding Generation": "FAILED",
        "Vector Upload": "FAILED",
        "Index Statistics": "FAILED"
    }

    # 1. Document Loading
    doc_status, docs_loaded, all_docs = test_document_loading()
    results["Document Loading"] = doc_status

    # 2. Chunk Generation
    chunk_status, chunks_gen, all_chunks = test_chunking(all_docs)
    results["Chunk Generation"] = chunk_status

    # 3. Embeddings Generation
    emb_status, embeds_gen, embedded_docs = test_embeddings(all_chunks)
    results["Embedding Generation"] = emb_status

    # 4. Pinecone Upload and Stats
    conn_status, up_status, stat_status, vectors_up, index_stats, pc_manager = test_pinecone_upload(embedded_docs)
    
    results["Pinecone Connection"] = conn_status
    results["Vector Upload"] = up_status
    results["Index Statistics"] = stat_status

    # Display results
    print_summary(
        docs_loaded, 
        chunks_gen, 
        embeds_gen, 
        vectors_up, 
        index_stats,
        results
    )
    
    # Optional Preview
    print_optional_preview(embedded_docs)
    
    # Optional Cleanup
    cleanup_prompt(pc_manager)


if __name__ == "__main__":
    main()
