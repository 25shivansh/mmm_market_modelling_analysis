"""
Test Script for KnowledgeTextChunker

Run:
    python tests/test_text_chunker.py
or
    python -m tests.test_text_chunker
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import colorama
from colorama import Fore, Style
from langchain_core.documents import Document

# Initialize colorama
colorama.init(autoreset=True)

# Determine the project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import core components
from src.knowledge_base.document_loader import DocumentLoader
from src.knowledge_base.text_chunker import KnowledgeTextChunker

# Configure logging for the test script
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def print_header() -> None:
    """Prints the test script header."""
    print(f"\n{Style.BRIGHT}{'=' * 52}")
    print(f"{Fore.CYAN}{Style.BRIGHT}TEXT CHUNKER VERIFICATION")
    print(f"{Style.BRIGHT}{'=' * 52}\n")


def display_statistics(
    all_docs: Dict[str, List[Document]],
    all_chunks: Dict[str, List[Document]],
) -> None:
    """Displays overall and per-domain chunking statistics."""
    
    total_docs = sum(len(docs) for docs in all_docs.values())
    total_chunks_list = []
    for chunks in all_chunks.values():
        total_chunks_list.extend(chunks)
        
    total_chunks_count = len(total_chunks_list)
    
    if total_chunks_count > 0:
        sizes = [len(c.page_content) for c in total_chunks_list]
        words = [len(c.page_content.split()) for c in total_chunks_list]
        avg_size = sum(sizes) / total_chunks_count
        largest = max(sizes)
        smallest = min(sizes)
        avg_words = sum(words) / total_chunks_count
    else:
        avg_size = largest = smallest = avg_words = 0

    print(f"{Fore.BLUE}{Style.BRIGHT}Overall Statistics")
    print(f"Documents Loaded       : {total_docs}")
    print(f"Chunks Generated       : {total_chunks_count}")
    print(f"Average Chunk Size     : {avg_size:.2f} characters")
    print(f"Largest Chunk          : {largest} characters")
    print(f"Smallest Chunk         : {smallest} characters")
    print(f"Average Words Per Chunk: {avg_words:.2f} words\n")

    for domain in ["mmm", "forecast", "sentiment"]:
        d_docs = all_docs.get(domain, [])
        d_chunks = all_chunks.get(domain, [])
        
        d_doc_count = len(d_docs)
        d_chunk_count = len(d_chunks)
        
        if d_chunk_count > 0:
            d_sizes = [len(c.page_content) for c in d_chunks]
            d_words = [len(c.page_content.split()) for c in d_chunks]
            d_avg_size = sum(d_sizes) / d_chunk_count
            d_avg_words = sum(d_words) / d_chunk_count
        else:
            d_avg_size = d_avg_words = 0
            
        print(f"{Fore.CYAN}{Style.BRIGHT}{domain.title()}")
        print(f"  Documents Loaded  : {d_doc_count}")
        print(f"  Chunks Generated  : {d_chunk_count}")
        print(f"  Average Chunk Size: {d_avg_size:.2f} characters")
        print(f"  Average Word Count: {d_avg_words:.2f} words\n")


def verify_metadata(chunk: Document) -> Tuple[bool, str]:
    """
    Verifies that the required metadata fields are present in the chunk.
    
    Args:
        chunk: The LangChain Document chunk.
        
    Returns:
        A tuple of (is_valid, error_message).
    """
    metadata = chunk.metadata
    
    prompt_keys = [
        "source", "file_name", "domain", "chunk_index",
        "total_chunks", "character_count", "word_count"
    ]
    
    missing_keys = [key for key in prompt_keys if key not in metadata]
    
    if missing_keys:
        return False, f"Missing metadata keys: {', '.join(missing_keys)}"
        
    return True, ""


def display_preview(chunk: Document) -> None:
    """Displays the metadata and a content preview for the first chunk."""
    print(f"{Fore.BLUE}{Style.BRIGHT}First Chunk Preview")
    print("Metadata:")
    for k, v in chunk.metadata.items():
        print(f"  - {k}: {v}")
        
    print("\nContent (First 300 characters):")
    preview = chunk.page_content[:300].replace("\n", " ")
    print(f"{Fore.LIGHTBLACK_EX}{preview}...\n")


def verify_chunks(all_docs: Dict[str, List[Document]], all_chunks: Dict[str, List[Document]]) -> Dict[str, str]:
    """
    Performs validation checks and returns the result statuses.
    """
    results = {
        "MMM": "WARNING",
        "Forecast": "WARNING",
        "Sentiment": "WARNING",
        "Metadata": "WARNING",
        "Chunking": "WARNING",
    }
    
    total_docs = sum(len(docs) for docs in all_docs.values())
    total_chunks_count = sum(len(chunks) for chunks in all_chunks.values())
    
    if total_docs > 0:
        results["Chunking"] = "PASS" if total_chunks_count > 0 else "FAILED"
    else:
        results["Chunking"] = "WARNING"
        
    for d_key, display_name in [("mmm", "MMM"), ("forecast", "Forecast"), ("sentiment", "Sentiment")]:
        d_chunks = all_chunks.get(d_key, [])
        if len(all_docs.get(d_key, [])) > 0:
            results[display_name] = "PASS" if len(d_chunks) > 0 else "FAILED"
        else:
            results[display_name] = "WARNING"
            
    # Verification of metadata and previews
    first_chunk = None
    for chunks in all_chunks.values():
        if chunks:
            first_chunk = chunks[0]
            break
            
    if first_chunk:
        display_preview(first_chunk)
        is_valid, err_msg = verify_metadata(first_chunk)
        if is_valid:
            results["Metadata"] = "PASS"
        else:
            results["Metadata"] = "FAILED"
            logger.warning(f"Metadata verification failed: {err_msg}")
    else:
        results["Metadata"] = "WARNING"
        
    return results


def print_final_summary(results: Dict[str, str]) -> None:
    """Prints the final verification summary."""
    print(f"{Style.BRIGHT}{'=' * 52}")
    print("TEXT CHUNKER VERIFICATION")
    print(f"{Style.BRIGHT}{'=' * 52}\n")

    all_passed = True
    any_failed = False

    for category, status in results.items():
        if status == "PASS":
            status_text = f"{Fore.GREEN}PASS"
        elif status == "WARNING":
            status_text = f"{Fore.YELLOW}WARNING"
            all_passed = False
        else:
            status_text = f"{Fore.RED}FAILED"
            all_passed = False
            any_failed = True

        print(f"{category:<15} {status_text}")

    print(f"\n{Style.BRIGHT}Overall Result")
    if not any_failed and all_passed:
        print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS")
    elif any_failed:
        print(f"{Fore.RED}{Style.BRIGHT}FAILED")
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}WARNING")
    print(f"{Style.BRIGHT}{'=' * 52}\n")


def main() -> None:
    """Main execution entry point for the test script."""
    print_header()

    try:
        loader = DocumentLoader(PROJECT_ROOT)
        all_docs = loader.load_all_documents()
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        all_docs = {"mmm": [], "forecast": [], "sentiment": []}
        
    try:
        chunker = KnowledgeTextChunker(chunk_size=1000, chunk_overlap=200)
    except Exception as e:
        logger.error(f"Failed to initialize KnowledgeTextChunker: {e}")
        return

    all_chunks: Dict[str, List[Document]] = {"mmm": [], "forecast": [], "sentiment": []}
    
    try:
        all_chunks["mmm"] = chunker.split_mmm_documents(all_docs.get("mmm", []))
        all_chunks["forecast"] = chunker.split_forecast_documents(all_docs.get("forecast", []))
        all_chunks["sentiment"] = chunker.split_sentiment_documents(all_docs.get("sentiment", []))
    except Exception as e:
        logger.error(f"Failed during chunking operations: {e}")
        
    display_statistics(all_docs, all_chunks)
    
    results = verify_chunks(all_docs, all_chunks)
    
    print_final_summary(results)


if __name__ == "__main__":
    main()
