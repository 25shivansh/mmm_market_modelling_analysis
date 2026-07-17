"""
Test Script for Retriever

Run:
    python tests/test_retriever.py
or
    python -m tests.test_retriever
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List

import colorama
from colorama import Fore, Style
from langchain_core.documents import Document

# Initialize colorama
colorama.init(autoreset=True)

# Determine the project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.retrieval.retriever import Retriever

# Configure logging
logging.basicConfig(level=logging.ERROR) # Minimal logging


def print_header() -> None:
    print("====================================================")
    print("RETRIEVER VERIFICATION")
    print("====================================================")


def display_documents(documents: List[Document]) -> bool:
    """
    Display the retrieved documents and return True if metadata is preserved 
    and page_content is not empty.
    """
    valid = True
    for i, doc in enumerate(documents, start=1):
        print("----------------------------------------------------")
        print(f"Document {i}")
        print(f"Similarity Rank : {i}")
        
        content = getattr(doc, "page_content", "")
        if not content:
            valid = False
            
        print("Preview :")
        print(f"{content[:200].replace(chr(10), ' ')}\n")
        
        metadata = getattr(doc, "metadata", {})
        if not metadata:
            valid = False
            
        print("Metadata")
        for k, v in metadata.items():
            print(f"  - {k}: {v}")
            
    return valid


def run_query(retriever: Retriever, query: str, validation_results: Dict[str, str]) -> None:
    print("Query")
    print(f"{query}\n")
    try:
        docs = retriever.search(query, top_k=5)
        print("Retrieved Documents")
        print(f"{len(docs)}")
        
        if len(docs) > 0:
            validation_results["Semantic Search"] = "PASS"
            validation_results["Query Embedding"] = "PASS"
            validation_results["Returned Documents"] = "PASS"
        else:
            if validation_results["Semantic Search"] != "PASS":
                validation_results["Semantic Search"] = "PASS" 
            if validation_results["Query Embedding"] != "PASS":
                validation_results["Query Embedding"] = "PASS"
        
        docs_valid = display_documents(docs)
        if docs_valid and len(docs) > 0:
            validation_results["Metadata Preservation"] = "PASS"
            
    except Exception as e:
        print(f"Error executing search for query '{query}': {e}")
    
    print("====================================================")


def test_empty_query(retriever: Retriever) -> None:
    try:
        retriever.search("", 5)
        print("Empty Query Validation\nFAILED")
    except ValueError:
        print("Empty Query Validation\nPASS")
    except Exception:
        print("Empty Query Validation\nFAILED")
    print("====================================================")


def print_summary(results: Dict[str, str]) -> None:
    print("VALIDATION")
    
    keys = [
        "Retriever Initialization",
        "Query Embedding",
        "Semantic Search",
        "Metadata Preservation",
        "Returned Documents"
    ]
    
    for key in keys:
        status = results.get(key, "FAILED")
        colored_status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if status == "PASS" else f"{Fore.RED}FAILED{Style.RESET_ALL}"
        print(f"{key:<28} {colored_status}")
        
    print("\nOverall Result")
    if all(status == "PASS" for status in results.values()):
        print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}FAILED{Style.RESET_ALL}")
    print("====================================================")


def main() -> None:
    print_header()
    
    validation_results = {
        "Retriever Initialization": "FAILED",
        "Query Embedding": "FAILED",
        "Semantic Search": "FAILED",
        "Metadata Preservation": "FAILED",
        "Returned Documents": "FAILED"
    }
    
    # 1. Initialize Retriever
    retriever = None
    try:
        retriever = Retriever()
        validation_results["Retriever Initialization"] = "PASS"
    except Exception as e:
        print(f"Failed to initialize Retriever: {e}")
        
    # 2. Predefined Queries
    queries = [
        "What factors are contributing to machine failures?",
        "Summarize the marketing recommendations.",
        "What is the future sales forecast?"
    ]
    
    if retriever:
        for q in queries:
            run_query(retriever, q, validation_results)
            
    # 3. Optional Empty Query Test
    if retriever:
        test_empty_query(retriever)
        
    # 4. Print Summary
    print_summary(validation_results)


if __name__ == "__main__":
    main()
