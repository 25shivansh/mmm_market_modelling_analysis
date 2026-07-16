"""
Test Script for DocumentLoader

Run:
    python tests/test_document_loader.py
or
    python -m tests.test_document_loader
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List

import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Determine the project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import Document Loader
from src.knowledge_base.document_loader import DocumentLoader
from langchain_core.documents import Document

# Configure logging for the test script
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def print_header() -> None:
    """Prints the test script header."""
    print(f"\n{Style.BRIGHT}{'=' * 70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Testing DocumentLoader Implementation")
    print(f"{Style.BRIGHT}{'=' * 70}\n")


def print_domain_summary(domain_name: str, documents: List[Document]) -> str:
    """
    Prints a summary for a specific knowledge domain.
    Returns the status ('PASS', 'WARNING', 'FAILED') to be used in the final summary.
    """
    print(f"\n{Style.BRIGHT}{'-' * 70}")
    print(f"{Fore.CYAN}Domain: {domain_name.upper()}")
    print(f"{Style.BRIGHT}{'-' * 70}")

    if not documents:
        print(f"{Fore.YELLOW}WARNING: No documents found for {domain_name}.")
        return "WARNING"

    total_docs = len(documents)
    total_chars = sum(len(doc.page_content) for doc in documents)
    total_words = sum(len(doc.page_content.split()) for doc in documents)

    print(f"Total Documents : {total_docs}")
    print(f"Total Characters: {total_chars:,}")
    print(f"Total Words     : {total_words:,}")

    return "PASS"


def print_document_preview(domain_name: str, documents: List[Document]) -> None:
    """Prints the metadata and content preview of the first document in the domain."""
    if not documents:
        return

    first_doc = documents[0]
    metadata = first_doc.metadata

    print(f"\n{Fore.BLUE}First Document Preview ({domain_name.upper()}):")
    print("Metadata:")
    print(f"  - Source          : {metadata.get('source', 'N/A')}")
    print(f"  - Filename        : {metadata.get('filename', 'N/A')}")
    print(f"  - Knowledge Domain: {metadata.get('knowledge_domain', 'N/A')}")
    print(f"  - Extension       : {metadata.get('extension', 'N/A')}")
    print(f"  - Relative Path   : {metadata.get('relative_path', 'N/A')}")

    print("\nContent (First 300 characters):")
    preview_content = first_doc.page_content[:300].replace("\n", " ")
    print(f"{Fore.LIGHTBLACK_EX}{preview_content}...")


def print_final_summary(results: Dict[str, str]) -> None:
    """Prints the final verification summary."""
    print(f"\n{Style.BRIGHT}{'=' * 52}")
    print("Document Loader Verification")
    print(f"{Style.BRIGHT}{'=' * 52}")

    all_passed = True

    for domain, status in results.items():
        if status == "PASS":
            status_text = f"{Fore.GREEN}PASS"
        elif status == "WARNING":
            status_text = f"{Fore.YELLOW}WARNING"
            all_passed = False
        else:
            status_text = f"{Fore.RED}FAILED"
            all_passed = False

        print(f"{domain:<15} {status_text}")

    print(f"\n{Style.BRIGHT}Overall Result")
    if all_passed:
        print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS")
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}WARNING / FAILED")
    print(f"{Style.BRIGHT}{'=' * 52}\n")


def main() -> None:
    """Main execution entry point for the test script."""
    print_header()

    results: Dict[str, str] = {
        "MMM": "FAILED",
        "Forecast": "FAILED",
        "Sentiment": "FAILED",
    }

    try:
        loader = DocumentLoader(PROJECT_ROOT)
        
        # Load documents gracefully
        try:
            all_docs = loader.load_all_documents()
        except Exception as e:
            logger.error(f"Error during document loading: {e}")
            all_docs = {}

        domains_map = {
            "MMM": all_docs.get("mmm", []),
            "Forecast": all_docs.get("forecast", []),
            "Sentiment": all_docs.get("sentiment", []),
        }

        for domain_name, docs in domains_map.items():
            try:
                status = print_domain_summary(domain_name, docs)
                results[domain_name] = status
                print_document_preview(domain_name, docs)
            except Exception as e:
                logger.error(f"Error processing domain {domain_name}: {e}")
                results[domain_name] = "FAILED"

    except Exception as e:
        logger.error(f"Critical failure initializing DocumentLoader: {e}")

    print_final_summary(results)


if __name__ == "__main__":
    main()