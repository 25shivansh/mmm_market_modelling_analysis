"""
Test Script for RAGPipeline

Run:
    python tests/test_rag_pipeline.py
or
    python -m tests.test_rag_pipeline
"""

import logging
import sys
from pathlib import Path

# Determine the project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.rag.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.ERROR) # Minimal logging


def run_test(pipeline: RAGPipeline, test_name: str, question: str, expect_empty: bool = False) -> None:
    """
    Helper function to execute test cases for the RAG pipeline.
    Handles standard flow, empty validations, and external rate limits gracefully.
    """
    print("-" * 60)
    print(test_name)
    print("-" * 60)
    print()
    
    try:
        if expect_empty:
            pipeline.generate_answer(question, top_k=5)
            # If it didn't raise ValueError, the test failed
            print("✗ FAILED\n")
            print("Empty question did not raise the expected exception.")
        else:
            result = pipeline.generate_answer(question, top_k=5)
            ans = result.get("answer", "")
            docs_count = result.get("retrieved_documents", 0)
            
            print("✓ PASSED\n")
            print(f"Retrieved Documents : {docs_count}\n")
            print("Answer\n")
            print(f"{ans}")
            
    except Exception as e:
        error_msg = str(e)
        error = error_msg.lower()
        
        rate_limit_indicators = [
            "429",
            "rate limit",
            "rate_limit",
            "rate_limit_exceeded",
            "too many requests"
        ]
        
        # Handle external Mistral API rate limit issues without failing the build
        if any(indicator in error for indicator in rate_limit_indicators):
            print("⚠ SKIPPED\n")
            print("Reason:")
            print("Mistral API rate limit exceeded (HTTP 429)\n")
            print("Details:")
            print(f"{error_msg}")
        elif expect_empty and isinstance(e, ValueError):
            print("✓ PASSED\n")
            print("Raised ValueError as expected.")
        else:
            print("✗ FAILED\n")
            print(f"{error_msg}")
            
    print("\n" + "-" * 60 + "\n")


def main() -> None:
    print("====================================================")
    print("RAG PIPELINE VERIFICATION")
    print("====================================================\n")
    
    try:
        pipeline = RAGPipeline()
    except Exception as e:
        print("-" * 60)
        print("Pipeline Initialization")
        print("-" * 60)
        print("\n✗ FAILED\n")
        print(f"Failed to initialize RAGPipeline: {e}")
        print("\n" + "-" * 60 + "\n")
        return

    # Existing test cases
    tests = [
        ("Marketing Recommendations", "Summarize the marketing recommendations."),
        ("Sales Forecast Test", "What is the expected sales forecast for the next 12 months?"),
        ("Business Insights", "What business insights are available?"),
        ("Customer Sentiment Trends", "Which customer sentiment trends are observed?"),
        ("Unknown Knowledge Handling", "What marketing budget should I allocate to television ads?")
    ]

    for test_name, question in tests:
        run_test(pipeline, test_name, question)
        
    run_test(pipeline, "Empty Question Validation", "", expect_empty=True)
    
    print("====================================================")
    print("TESTING COMPLETED")
    print("====================================================")


if __name__ == "__main__":
    main()
