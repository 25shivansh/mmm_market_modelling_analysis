"""
Standalone diagnostic script to display the complete contents of the Marketing Recommendations Report.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.report_repository import ReportRepository


def main():
    repo = ReportRepository()

    reports = repo.get_reports()
    target_report = None
    for r in reports:
        if r.get("title") == "Marketing Recommendations Report":
            target_report = r
            break

    print("========================================")
    print("Marketing Recommendations Report")
    print("========================================\n")

    if not target_report:
        print("Report 'Marketing Recommendations Report' not found in MongoDB.")
        return

    title = target_report.get("title", "")
    category = target_report.get("category", "")
    metadata = target_report.get("metadata", {})
    content = target_report.get("content", "")

    char_count = len(content)
    word_count = len(content.split())

    print(f"Title          : {title}")
    print(f"Category       : {category}")
    print(f"Metadata       : {metadata}")
    print(f"Content Length : {char_count} characters\n")

    print("----------------------------------------")
    print("FULL REPORT CONTENT:")
    print("----------------------------------------")
    print(content)
    print("----------------------------------------\n")

    print(f"Total Characters : {char_count}")
    print(f"Total Words      : {word_count}\n")

    print("========================================")
    print("SUMMARY")
    print("========================================")
    
    # Identify distinct recommendation items in the body
    body_lines = [
        line.strip() for line in content.splitlines()
        if line.strip() and not line.startswith("=") and "REPORT" not in line
    ]
    recommendation_items = [
        line for line in body_lines
        if line.startswith("-") or line.startswith("*") or line.startswith("1.") or line.startswith("2.")
    ]
    has_multiple = len(recommendation_items) > 1
    answer = "YES" if has_multiple else "NO"

    print(f"Does the report contain multiple recommendations?\n{answer}")
    print("========================================")


if __name__ == "__main__":
    main()
