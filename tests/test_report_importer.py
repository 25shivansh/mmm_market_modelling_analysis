"""
Standalone integration test for ReportImporter using real MongoDB service.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.report_repository import ReportRepository
from src.knowledge_reports.report_importer import ReportImporter


def run_tests():
    repo = ReportRepository()

    passed = 0
    failed = 0
    total = 7

    def record_result(name, action):
        nonlocal passed, failed
        try:
            action()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    # TEST 1: Initialize ReportImporter
    importer = None
    def test1():
        nonlocal importer
        importer = ReportImporter(repo=repo)
        if importer is None or importer.repo is None:
            raise AssertionError("ReportImporter failed to initialize.")
    record_result("Importer initialized", test1)

    # TEST 2: Count reports in MongoDB before import
    initial_count = 0
    def test2():
        nonlocal initial_count
        initial_count = repo.count_reports()
        if not isinstance(initial_count, int):
            raise AssertionError(f"Expected integer for count, got {type(initial_count)}")
    record_result("Count before import", test2)

    # TEST 3: import_reports("reports")
    imported_count = 0
    def test3():
        nonlocal imported_count
        imported_count = importer.import_reports("reports")
        if not isinstance(imported_count, int) or imported_count < 0:
            raise AssertionError(f"Expected non-negative integer, got {imported_count}")
    record_result("Reports imported", test3)

    # TEST 4: MongoDB updated
    def test4():
        final_count = repo.count_reports()
        if not isinstance(final_count, int):
            raise AssertionError(f"Expected integer for final count, got {type(final_count)}")
        if final_count < initial_count:
            raise AssertionError(f"Expected final_count ({final_count}) >= initial_count ({initial_count})")
        if final_count != initial_count + imported_count:
            raise AssertionError(
                f"Expected final_count ({final_count}) == initial_count ({initial_count}) + imported_count ({imported_count})"
            )
    record_result("MongoDB updated", test4)

    # TEST 5: Duplicate protection
    def test5():
        reimport_count = importer.import_reports("reports")
        if reimport_count != 0:
            raise AssertionError(f"Expected 0 new reports on re-import, got {reimport_count}")
    record_result("Duplicate protection", test5)

    # TEST 6: Imported reports verified
    def test6():
        all_reports = repo.get_reports()
        existing_filenames = set()
        for r in all_reports:
            meta = r.get("metadata", {})
            if isinstance(meta, dict) and "filename" in meta:
                existing_filenames.add(meta["filename"])

        expected_stems = [
            "business_insights_report",
            "marketing_recommendations_report",
            "data_understanding_report",
            "forecast_summary",
            "sentiment_predictions",
        ]

        reports_dir = Path("reports")
        for stem in expected_stems:
            matching_files = [f.name for f in reports_dir.glob(f"{stem}.*")]
            for filename in matching_files:
                if filename not in existing_filenames:
                    raise AssertionError(f"Report file '{filename}' was not found in MongoDB repository.")
    record_result("Imported reports verified", test6)

    # TEST 7: Validation
    def test7():
        for invalid in [None, "non_existent_directory_98765", 123]:
            try:
                importer.import_reports(invalid)
                raise AssertionError(f"Expected ValueError for import_reports({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for import_reports({invalid}), got {type(e)}")

        for invalid in [None, "non_existent_file_98765.txt", 123]:
            try:
                importer.import_report(invalid)
                raise AssertionError(f"Expected ValueError for import_report({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for import_report({invalid}), got {type(e)}")
    record_result("Validation", test7)

    # Summary
    print("\n=====================================")
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=====================================\n")

    if passed == total:
        print("ReportImporter integration tests completed successfully.")


if __name__ == "__main__":
    run_tests()
