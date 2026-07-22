"""
Standalone integration test for PromptBuilder.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.documents import Document
from src.rag.prompt_builder import PromptBuilder


def run_tests():
    # Sample documents
    doc1 = Document(
        page_content="Marketing campaign performance increased by 15% during Q2.",
        metadata={"report_id": "report_001", "category": "marketing", "chunk_index": 0}
    )
    doc2 = Document(
        page_content="Customer satisfaction improved significantly after the loyalty program launch.",
        metadata={"report_id": "report_002", "category": "customer", "chunk_index": 1}
    )
    doc3 = Document(
        page_content="Forecasts predict a 10% increase in revenue next quarter.",
        metadata={"report_id": "report_003", "category": "forecast", "chunk_index": 0}
    )
    documents = [doc1, doc2, doc3]
    question = "What improved during Q2?"

    passed = 0
    failed = 0
    total = 9

    def record_result(name, action):
        nonlocal passed, failed
        try:
            action()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    # TEST 1: Initialize PromptBuilder
    builder = None
    def test1():
        nonlocal builder
        builder = PromptBuilder()
        if builder is None:
            raise AssertionError("PromptBuilder failed to initialize.")
    record_result("PromptBuilder initialized", test1)

    # TEST 2: build_context(documents)
    context_str = ""
    def test2():
        nonlocal context_str
        context_str = builder.build_context(documents)
        if not isinstance(context_str, str):
            raise AssertionError(f"Expected string, got {type(context_str)}")
        for doc in documents:
            if doc.page_content not in context_str:
                raise AssertionError(f"Document content '{doc.page_content}' missing from context.")
        if "Document 1" not in context_str or "Document 2" not in context_str or "Document 3" not in context_str:
            raise AssertionError("Document numbering missing from context.")
    record_result("Build context", test2)

    # TEST 3: build_rag_prompt()
    generated_prompt = ""
    def test3():
        nonlocal generated_prompt
        generated_prompt = builder.build_rag_prompt(question, documents)
        if not isinstance(generated_prompt, str):
            raise AssertionError(f"Expected string, got {type(generated_prompt)}")
        required_sections = ["MarketMind AI", "Context", "Question", "Answer"]
        for section in required_sections:
            if section not in generated_prompt:
                raise AssertionError(f"Required section '{section}' missing from generated prompt.")
    record_result("Build prompt", test3)

    # TEST 4: Context included
    def test4():
        for doc in documents:
            if doc.page_content not in generated_prompt:
                raise AssertionError(f"Document content '{doc.page_content}' missing from prompt.")
    record_result("Context included", test4)

    # TEST 5: Question included
    def test5():
        if question not in generated_prompt:
            raise AssertionError(f"Question '{question}' missing from generated prompt.")
    record_result("Question included", test5)

    # TEST 6: Empty context
    def test6():
        empty_ctx = builder.build_context([])
        if empty_ctx != "No relevant documents found.":
            raise AssertionError(f"Expected 'No relevant documents found.', got '{empty_ctx}'")
    record_result("Empty context", test6)

    # TEST 7: Empty prompt
    def test7():
        empty_prompt = builder.build_rag_prompt(question, [])
        if not isinstance(empty_prompt, str) or not empty_prompt:
            raise AssertionError("Failed to generate prompt for empty document list.")
        if "No relevant documents found." not in empty_prompt:
            raise AssertionError("Expected 'No relevant documents found.' in generated prompt.")
    record_result("Empty prompt", test7)

    # TEST 8: Validation question
    def test8():
        for inv_q in [None, "", 123]:
            try:
                builder.build_rag_prompt(inv_q, documents)
                raise AssertionError(f"Expected ValueError for question {inv_q}")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for question {inv_q}, got {type(e)}")
    record_result("Validation question", test8)

    # TEST 9: Validation documents
    def test9():
        for inv_docs in [None, 123]:
            try:
                builder.build_context(inv_docs)
                raise AssertionError(f"Expected ValueError for build_context({inv_docs})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for build_context({inv_docs}), got {type(e)}")

            try:
                builder.build_rag_prompt(question, inv_docs)
                raise AssertionError(f"Expected ValueError for build_rag_prompt({question}, {inv_docs})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for build_rag_prompt({question}, {inv_docs}), got {type(e)}")
    record_result("Validation documents", test9)

    # Summary
    print("\n=====================================")
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=====================================\n")

    if passed == total:
        print("PromptBuilder integration tests completed successfully.")


if __name__ == "__main__":
    run_tests()
