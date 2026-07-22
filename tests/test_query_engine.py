"""
Standalone integration test for QueryEngine using real Pinecone service.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.documents import Document
from src.rag.query_engine import QueryEngine


def run_tests():
    passed = 0
    failed = 0
    total = 8

    def record_result(name, action):
        nonlocal passed, failed
        try:
            action()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    # TEST 1: Initialize QueryEngine
    engine = None
    def test1():
        nonlocal engine
        engine = QueryEngine()
        if engine is None or engine.retriever is None:
            raise AssertionError("QueryEngine failed to initialize.")
    record_result("QueryEngine initialized", test1)

    # TEST 2: search()
    def test2():
        results = engine.search("marketing performance")
        if not isinstance(results, list):
            raise AssertionError(f"Expected list, got {type(results)}")
        if len(results) <= 0:
            raise AssertionError(f"Expected list length > 0, got {len(results)}")
        for doc in results:
            if not isinstance(doc, Document):
                raise AssertionError(f"Expected object of type Document, got {type(doc)}")
    record_result("Search", test2)

    # TEST 3: count_results()
    def test3():
        query = "marketing performance"
        count = engine.count_results(query)
        if not isinstance(count, int):
            raise AssertionError(f"Expected integer, got {type(count)}")
        if count <= 0:
            raise AssertionError(f"Expected count > 0, got {count}")
        search_docs = engine.search(query)
        if count != len(search_docs):
            raise AssertionError(f"Expected count ({count}) == len(search(query)) ({len(search_docs)})")
    record_result("Count results", test3)

    # TEST 4: search_with_scores()
    def test4():
        results = engine.search_with_scores("marketing performance")
        if not isinstance(results, list):
            raise AssertionError(f"Expected list, got {type(results)}")
        if len(results) <= 0:
            raise AssertionError(f"Expected list length > 0, got {len(results)}")
        for item in results:
            if not isinstance(item, tuple) or len(item) != 2:
                raise AssertionError(f"Expected tuple of (Document, score), got {item}")
            doc, score = item
            if not isinstance(doc, Document):
                raise AssertionError(f"Expected Document in tuple, got {type(doc)}")
            if not isinstance(score, (int, float)):
                raise AssertionError(f"Expected numeric score, got {type(score)}")
    record_result("Search with scores", test4)

    # TEST 5: Search using a query that should not exist
    def test5():
        query = "qwertyuiopabcdefgh123456789"
        res_search = engine.search(query)
        res_count = engine.count_results(query)
        res_scores = engine.search_with_scores(query)

        if not isinstance(res_search, list):
            raise AssertionError(f"Expected search() to return a list, got {type(res_search)}")
        if not isinstance(res_count, int):
            raise AssertionError(f"Expected count_results() to return an int, got {type(res_count)}")
        if not isinstance(res_scores, list):
            raise AssertionError(f"Expected search_with_scores() to return a list, got {type(res_scores)}")

        if res_search == [] and res_count == 0 and res_scores == []:
            pass
        else:
            if res_count != len(res_search) or len(res_search) != len(res_scores):
                raise AssertionError("Mismatch in results count for query.")
    record_result("No results", test5)

    # TEST 6: Validation search()
    def test6():
        for invalid in [None, "", 123]:
            try:
                engine.search(invalid)
                raise AssertionError(f"Expected ValueError for search({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for search({invalid}), got {type(e)}")
    record_result("Validation search", test6)

    # TEST 7: Validation search_with_scores()
    def test7():
        for invalid in [None, "", 123]:
            try:
                engine.search_with_scores(invalid)
                raise AssertionError(f"Expected ValueError for search_with_scores({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for search_with_scores({invalid}), got {type(e)}")
    record_result("Validation search_with_scores", test7)

    # TEST 8: Validation count_results()
    def test8():
        for invalid in [None, "", 123]:
            try:
                engine.count_results(invalid)
                raise AssertionError(f"Expected ValueError for count_results({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for count_results({invalid}), got {type(e)}")
    record_result("Validation count_results", test8)

    # Summary
    print("\n=====================================")
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=====================================\n")

    if passed == total:
        print("QueryEngine integration tests completed successfully.")


if __name__ == "__main__":
    run_tests()
