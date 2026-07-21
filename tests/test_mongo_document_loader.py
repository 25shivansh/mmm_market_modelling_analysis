import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.documents import Document

from src.database.report_repository import ReportRepository
from src.knowledge_base.mongo_document_loader import MongoDocumentLoader


def run_tests():
    repo = ReportRepository()

    # Clean database before tests
    repo.delete_all_reports()

    # Insert sample data
    id1 = repo.save_report(
        category="marketing",
        title="Marketing Performance Report",
        content="Marketing campaign performance improved by 15%.",
        metadata={"department": "Marketing"}
    )
    id2 = repo.save_report(
        category="forecast",
        title="Sales Forecast Report",
        content="Sales are expected to increase by 10% next quarter.",
        metadata={"region": "North"}
    )
    id3 = repo.save_report(
        category="marketing",
        title="Customer Engagement Report",
        content="Customer engagement increased across social media campaigns.",
        metadata={"platform": "Instagram"}
    )

    passed = 0
    failed = 0
    total = 14

    def record_result(name, action):
        nonlocal passed, failed
        try:
            action()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    # Test 1: Initialize loader
    loader = None
    def test1():
        nonlocal loader
        loader = MongoDocumentLoader(repo)
        if loader is None or loader.repository is None:
            raise AssertionError("Loader failed to initialize.")
    record_result("Loader initialized", test1)

    # Test 2: count_documents()
    def test2():
        count = loader.count_documents()
        if count != 3:
            raise AssertionError(f"Expected count 3, got {count}")
    record_result("Count documents", test2)

    # Test 3: load_all_documents()
    all_docs = []
    def test3():
        nonlocal all_docs
        all_docs = loader.load_all_documents()
        if not isinstance(all_docs, list):
            raise AssertionError("Expected list output.")
        if len(all_docs) != 3:
            raise AssertionError(f"Expected 3 documents, got {len(all_docs)}")
        if not all(isinstance(doc, Document) for doc in all_docs):
            raise AssertionError("Not all items are LangChain Document objects.")
    record_result("Load all documents", test3)

    # Test 4: Verify page_content
    def test4():
        for doc in all_docs:
            if not doc.page_content or not doc.page_content.strip():
                raise AssertionError("Document page_content is empty.")
    record_result("Verify page_content", test4)

    # Test 5: Verify metadata standard fields
    def test5():
        required_keys = {"report_id", "category", "title", "created_at", "updated_at"}
        for doc in all_docs:
            missing = required_keys - set(doc.metadata.keys())
            if missing:
                raise AssertionError(f"Document metadata missing keys: {missing}")
    record_result("Verify metadata", test5)

    # Test 6: Verify custom metadata
    def test6():
        departments = [doc.metadata.get("department") for doc in all_docs if "department" in doc.metadata]
        regions = [doc.metadata.get("region") for doc in all_docs if "region" in doc.metadata]
        platforms = [doc.metadata.get("platform") for doc in all_docs if "platform" in doc.metadata]

        if "Marketing" not in departments:
            raise AssertionError("Custom metadata 'department': 'Marketing' not found.")
        if "North" not in regions:
            raise AssertionError("Custom metadata 'region': 'North' not found.")
        if "Instagram" not in platforms:
            raise AssertionError("Custom metadata 'platform': 'Instagram' not found.")
    record_result("Verify custom metadata", test6)

    # Test 7: load_documents_by_category("marketing")
    def test7():
        mkt_docs = loader.load_documents_by_category("marketing")
        if len(mkt_docs) != 2:
            raise AssertionError(f"Expected 2 marketing documents, got {len(mkt_docs)}")
    record_result("Load documents by category marketing", test7)

    # Test 8: load_documents_by_category("forecast")
    def test8():
        fc_docs = loader.load_documents_by_category("forecast")
        if len(fc_docs) != 1:
            raise AssertionError(f"Expected 1 forecast document, got {len(fc_docs)}")
    record_result("Load documents by category forecast", test8)

    # Test 9: load_documents_by_category("unknown")
    def test9():
        unk_docs = loader.load_documents_by_category("unknown")
        if unk_docs != []:
            raise AssertionError(f"Expected empty list, got {unk_docs}")
    record_result("Load documents by category unknown", test9)

    # Test 10: load_document(report_id)
    def test10():
        doc = loader.load_document(str(id1))
        if doc is None:
            raise AssertionError("Document not returned for valid report_id.")
        if doc.metadata.get("title") != "Marketing Performance Report":
            raise AssertionError(f"Unexpected title: {doc.metadata.get('title')}")
        if doc.page_content != "Marketing campaign performance improved by 15%.":
            raise AssertionError("Content mismatch.")
        if doc.metadata.get("department") != "Marketing":
            raise AssertionError("Custom metadata department mismatch.")
    record_result("Load document by report_id", test10)

    # Test 11: Invalid report id ("000000000000000000000000")
    def test11():
        doc = loader.load_document("000000000000000000000000")
        if doc is not None:
            raise AssertionError("Expected None for non-existent report_id.")
    record_result("Load document with non-existent report_id", test11)

    # Test 12: Invalid category input
    def test12():
        invalid_inputs = [None, 123, ""]
        for val in invalid_inputs:
            try:
                loader.load_documents_by_category(val)
                raise AssertionError(f"Expected ValueError for invalid category {val}")
            except ValueError:
                pass
    record_result("Invalid category input validation", test12)

    # Test 13: Invalid report_id input
    def test13():
        invalid_inputs = [None, 123, ""]
        for val in invalid_inputs:
            try:
                loader.load_document(val)
                raise AssertionError(f"Expected ValueError for invalid report_id {val}")
            except ValueError:
                pass
    record_result("Invalid report_id input validation", test13)

    # Test 14: Empty database
    def test14():
        repo.delete_all_reports()
        empty_docs = loader.load_all_documents()
        if empty_docs != []:
            raise AssertionError(f"Expected empty list from load_all_documents(), got {empty_docs}")
        empty_count = loader.count_documents()
        if empty_count != 0:
            raise AssertionError(f"Expected count 0, got {empty_count}")
    record_result("Empty database test", test14)

    # Clean database after tests
    repo.delete_all_reports()

    # Print Summary
    print("\n====================================")
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("====================================\n")

    if passed == total:
        print("MongoDocumentLoader integration tests completed successfully.")


if __name__ == "__main__":
    run_tests()
