"""
Integration tests for KnowledgeSync using real MongoDB and Pinecone services.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.report_repository import ReportRepository
from src.knowledge_base.mongo_document_loader import MongoDocumentLoader
from src.knowledge_base.knowledge_sync import KnowledgeSync


def run_tests():
    repo = ReportRepository()

    # Load existing reports from MongoDB
    existing_reports = repo.get_reports()
    if not existing_reports:
        print("No reports available in MongoDB. Import reports before running this integration test.")
        sys.exit(1)

    expected_total_reports = len(existing_reports)

    # Extract available categories and a valid report ID from real MongoDB data
    categories = list(dict.fromkeys(r.get("category") for r in existing_reports if r.get("category")))
    valid_category_1 = categories[0] if categories else "marketing"
    valid_category_2 = categories[1] if len(categories) > 1 else valid_category_1

    valid_report_id = str(existing_reports[0]["_id"])

    passed = 0
    failed = 0
    total = 13

    def record_result(name, action):
        nonlocal passed, failed
        try:
            action()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    # Test 1: Initialize KnowledgeSync
    sync = None
    def test1():
        nonlocal sync
        sync = KnowledgeSync()
        if sync is None or sync.loader is None:
            raise AssertionError("KnowledgeSync failed to initialize.")
    record_result("KnowledgeSync initialized", test1)

    # Test 2: count_reports()
    def test2():
        count = sync.count_reports()
        if count != expected_total_reports:
            raise AssertionError(f"Expected {expected_total_reports} reports, got {count}")
    record_result("Count reports", test2)

    # Test 3: count_chunks()
    def test3():
        loader = MongoDocumentLoader(repo)
        docs = loader.load_all_documents()
        chunks_count = sync.count_chunks(docs)
        if not isinstance(chunks_count, int) or chunks_count <= 0:
            raise AssertionError(f"Expected chunk count > 0, got {chunks_count}")
    record_result("Count chunks", test3)

    # Test 4: sync_all_reports()
    def test4():
        uploaded = sync.sync_all_reports()
        if not isinstance(uploaded, int) or uploaded <= 0:
            raise AssertionError(f"Expected uploaded count > 0, got {uploaded}")
    record_result("Sync all reports", test4)

    # Test 5: sync_category(valid_category_1)
    def test5():
        mkt_uploaded = sync.sync_category(valid_category_1)
        if not isinstance(mkt_uploaded, int) or mkt_uploaded <= 0:
            raise AssertionError(f"Expected uploaded count > 0, got {mkt_uploaded}")
    record_result(f"Sync category {valid_category_1}", test5)

    # Test 6: sync_category(valid_category_2)
    def test6():
        fc_uploaded = sync.sync_category(valid_category_2)
        if not isinstance(fc_uploaded, int) or fc_uploaded <= 0:
            raise AssertionError(f"Expected uploaded count > 0, got {fc_uploaded}")
    record_result(f"Sync category {valid_category_2}", test6)

    # Test 7: sync_category("unknown")
    def test7():
        unk_uploaded = sync.sync_category("nonexistent_category_xyz")
        if unk_uploaded != 0:
            raise AssertionError(f"Expected 0 for unknown category, got {unk_uploaded}")
    record_result("Sync category unknown", test7)

    # Test 8: sync_report(report_id)
    def test8():
        rep_uploaded = sync.sync_report(valid_report_id)
        if not isinstance(rep_uploaded, int) or rep_uploaded <= 0:
            raise AssertionError(f"Expected uploaded count > 0, got {rep_uploaded}")
    record_result("Sync report by ID", test8)

    # Test 9: sync_report with non-existent report_id
    def test9():
        non_existent = sync.sync_report("000000000000000000000000")
        if non_existent != 0:
            raise AssertionError(f"Expected 0 for non-existent report_id, got {non_existent}")
    record_result("Sync non-existent report ID", test9)

    # Test 10: Validation for sync_category
    def test10():
        for invalid in [None, 123, ""]:
            try:
                sync.sync_category(invalid)
                raise AssertionError(f"Expected ValueError for category {invalid}")
            except ValueError:
                pass
    record_result("Validation sync_category", test10)

    # Test 11: Validation for sync_report
    def test11():
        for invalid in [None, 123, ""]:
            try:
                sync.sync_report(invalid)
                raise AssertionError(f"Expected ValueError for report_id {invalid}")
            except ValueError:
                pass
    record_result("Validation sync_report", test11)

    # Test 12: Empty database
    def test12():
        empty_repo = ReportRepository()
        empty_repo._collection = repo._db_manager.get_collection("_temp_empty_test_collection")
        try:
            empty_sync = KnowledgeSync(loader=MongoDocumentLoader(empty_repo))
            c = empty_sync.count_reports()
            if c != 0:
                raise AssertionError(f"Expected 0 reports, got {c}")
            u = empty_sync.sync_all_reports()
            if u != 0:
                raise AssertionError(f"Expected 0 synced reports, got {u}")
        finally:
            empty_repo._collection.drop()
    record_result("Empty database", test12)

    # Test 13: Verify deterministic vector IDs
    def test13():
        # STEP 1: First synchronization
        uploaded_1 = sync.sync_all_reports()
        if not isinstance(uploaded_1, int) or uploaded_1 <= 0:
            raise AssertionError(f"Expected uploaded count > 0, got {uploaded_1}")
        print("[PASS] First synchronization")

        # STEP 2: Fetch initial vector count
        stats1 = sync.pinecone_manager.get_index_stats()
        first_vector_count = stats1.get("total_vector_count", stats1.get("total_vectors", 0))
        if first_vector_count <= 0:
            raise AssertionError(f"Expected first_vector_count > 0, got {first_vector_count}")
        print("[PASS] Initial vector count")

        # STEP 3: Second synchronization without modifying MongoDB
        uploaded_2 = sync.sync_all_reports()
        if not isinstance(uploaded_2, int) or uploaded_2 <= 0:
            raise AssertionError(f"Expected uploaded count > 0, got {uploaded_2}")
        print("[PASS] Second synchronization")

        # STEP 4: Fetch vector count again and verify no duplicate vectors created
        stats2 = sync.pinecone_manager.get_index_stats()
        second_vector_count = stats2.get("total_vector_count", stats2.get("total_vectors", 0))
        if first_vector_count != second_vector_count:
            raise AssertionError(
                f"Expected first_vector_count ({first_vector_count}) == second_vector_count ({second_vector_count})"
            )
        print("[PASS] No duplicate vectors created")

    record_result("Verify deterministic vector IDs", test13)

    # Print Summary
    print("\n=====================================")
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=====================================\n")

    if passed == total:
        print("""=====================================

KnowledgeSync integration tests completed successfully.

Pinecone vectors have been preserved for inspection.

Run:

python tests/check_pinecone_contents.py

to verify indexed documents.

=====================================""")


if __name__ == "__main__":
    run_tests()
