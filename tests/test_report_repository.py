import sys
import time
from datetime import datetime
from bson.objectid import ObjectId

from src.database.report_repository import ReportRepository


def print_header(title: str) -> None:
    print("-" * 50)
    print(f"Running {title}")
    print("-" * 50)


def test_save_report(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    oid = repo.save_report(
        category="marketing",
        title="Marketing Performance Report",
        content="Google Ads delivered the highest ROI during Q2 while Facebook Ads showed declining ROAS.",
        metadata={
            "model": "Robyn",
            "version": "1.0",
            "generated_by": "KnowledgeReportGenerator"
        }
    )
    if not isinstance(oid, ObjectId):
        raise AssertionError("Returns ObjectId failed.")
    
    report = repo.get_report(oid)
    if not report:
        raise AssertionError("Report inserted failed.")


def test_retrieve_report_by_id(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    oid = repo.save_report(
        category="sales",
        title="Marketing Performance Report",
        content="Google Ads delivered the highest ROI during Q2 while Facebook Ads showed declining ROAS."
    )
    report = repo.get_report(oid)
    
    if report is None:
        raise AssertionError("Report not found.")
    if report["title"] != "Marketing Performance Report":
        raise AssertionError("Correct title failed.")
    if report["category"] != "sales":
        raise AssertionError("Correct category failed.")
    if report["content"] != "Google Ads delivered the highest ROI during Q2 while Facebook Ads showed declining ROAS.":
        raise AssertionError("Correct content failed.")


def test_retrieve_all_reports(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    
    repo.save_report("risk", "Risk 1", "Content 1")
    time.sleep(0.01)
    repo.save_report("risk", "Risk 2", "Content 2")
    
    reports = repo.get_reports()
    if not isinstance(reports, list):
        raise AssertionError("Returns list failed.")
    if len(reports) < 2:
        raise AssertionError("At least one report exists failed.")
    if reports[0]["title"] != "Risk 2":
        raise AssertionError("Sorted newest first failed.")


def test_retrieve_reports_by_category(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    repo.save_report("customer", "Cust 1", "Content 1")
    repo.save_report("customer", "Cust 2", "Content 2")
    repo.save_report("forecast", "Fore 1", "Content 3")
    
    reports = repo.get_reports_by_category("customer")
    if len(reports) != 2:
        raise AssertionError("Expected 2 reports for category 'customer'.")
    for r in reports:
        if r["category"] != "customer":
            raise AssertionError("Only requested category returned failed.")


def test_update_report(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    oid = repo.save_report("marketing", "Old Title", "Old Content", {"old": "meta"})
    original_report = repo.get_report(oid)
    
    time.sleep(0.01)
    
    success = repo.update_report(oid, content="New Content", metadata={"new": "meta"})
    if not success:
        raise AssertionError("Update succeeds failed.")
        
    updated = repo.get_report(oid)
    if updated["content"] != "New Content":
        raise AssertionError("New content stored failed.")
    if updated["metadata"] != {"new": "meta"}:
        raise AssertionError("Metadata update failed.")
    if updated["updated_at"] <= original_report["updated_at"]:
        raise AssertionError("updated_at changes failed.")


def test_count_reports(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    repo.save_report("marketing", "T1", "C1")
    repo.save_report("sales", "T2", "C2")
    
    if repo.count_reports() != 2:
        raise AssertionError("Count reports returned incorrect number.")


def test_delete_report(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    oid = repo.save_report("marketing", "T1", "C1")
    
    success = repo.delete_report(oid)
    if not success:
        raise AssertionError("Returns True failed.")
        
    if repo.get_report(oid) is not None:
        raise AssertionError("Report no longer exists failed.")


def test_delete_all_reports(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    repo.save_report("marketing", "T1", "C1")
    repo.save_report("sales", "T2", "C2")
    
    deleted_count = repo.delete_all_reports()
    if deleted_count != 2:
        raise AssertionError("Deleted count is correct failed.")
    if repo.count_reports() != 0:
        raise AssertionError("Collection becomes empty failed.")


def test_invalid_report_id_handling(repo: ReportRepository) -> None:
    # We pass strings that aren't valid ObjectIds, integers, and None
    invalid_ids = ["abc", 123, None, "5f5b5b5b5b5b5b5b5b5b5b5b5"]
    for invalid_id in invalid_ids:
        try:
            repo.get_report(invalid_id)
            raise AssertionError(f"Expected exception for id: {invalid_id}")
        except (ValueError, TypeError):
            pass


def test_invalid_input_validation(repo: ReportRepository) -> None:
    # Empty title
    try:
        repo.save_report("cat", "", "cont")
        raise AssertionError("Empty title should raise error.")
    except ValueError:
        pass

    # Empty category
    try:
        repo.save_report("", "title", "cont")
        raise AssertionError("Empty category should raise error.")
    except ValueError:
        pass

    # Empty content
    try:
        repo.save_report("cat", "title", " ")
        raise AssertionError("Empty content should raise error.")
    except ValueError:
        pass
        
    # Wrong argument types
    try:
        repo.save_report(123, "title", "cont")
        raise AssertionError("Wrong argument type for category should raise error.")
    except TypeError:
        pass


def test_metadata_persistence(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    meta = {
        "model": "Robyn",
        "version": "1.0",
        "generated_by": "KnowledgeReportGenerator",
        "metrics": {"roi": 1.5}
    }
    oid = repo.save_report("marketing", "Meta Test", "Content", meta)
    doc = repo.get_report(oid)
    if doc["metadata"] != meta:
        raise AssertionError("Metadata stored in MongoDB exactly matches input failed.")


def test_timestamp_creation(repo: ReportRepository) -> None:
    repo.delete_all_reports()
    oid = repo.save_report("marketing", "Time Test", "Content")
    doc = repo.get_report(oid)
    
    if "created_at" not in doc:
        raise AssertionError("created_at exists failed.")
    if "updated_at" not in doc:
        raise AssertionError("updated_at exists failed.")
    if not isinstance(doc["created_at"], datetime):
        raise AssertionError("created_at is datetime failed.")
    if not isinstance(doc["updated_at"], datetime):
        raise AssertionError("updated_at is datetime failed.")


def main():
    repo = ReportRepository()
    
    print("=" * 50)
    print("ReportRepository Integration Tests")
    print("=" * 50)
    
    # Test Isolation: Delete every document before running tests
    repo.delete_all_reports()
    
    tests = [
        ("Save Report Test", test_save_report),
        ("Retrieve Report By ID Test", test_retrieve_report_by_id),
        ("Retrieve All Reports Test", test_retrieve_all_reports),
        ("Retrieve Reports By Category Test", test_retrieve_reports_by_category),
        ("Update Report Test", test_update_report),
        ("Count Reports Test", test_count_reports),
        ("Delete Report Test", test_delete_report),
        ("Delete All Reports Test", test_delete_all_reports),
        ("Invalid Report ID Handling Test", test_invalid_report_id_handling),
        ("Invalid Input Validation Test", test_invalid_input_validation),
        ("Metadata Persistence Test", test_metadata_persistence),
        ("Timestamp Creation Test", test_timestamp_creation),
    ]

    tests_passed = 0
    tests_failed = 0

    for name, func in tests:
        print_header(name)
        try:
            func(repo)
            print("PASS\n")
            tests_passed += 1
        except Exception as e:
            print(f"FAIL: {e}\n")
            tests_failed += 1

    # Test Isolation: Delete every document after all tests finish
    repo.delete_all_reports()

    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Total Tests : {len(tests)}")
    print(f"Passed      : {tests_passed}")
    print(f"Failed      : {tests_failed}")
    print("=" * 50)

    if tests_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
