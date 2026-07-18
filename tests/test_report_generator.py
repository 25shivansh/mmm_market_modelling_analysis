import sys
from bson.objectid import ObjectId

from src.knowledge_reports.report_generator import ReportGenerator
from src.database.report_repository import ReportRepository


def print_header(title: str) -> None:
    print("-" * 50)
    print(f"Running {title}")
    print("-" * 50)


def verify_report(repo: ReportRepository, oid: ObjectId, expected_category: str, expected_title: str):
    if not isinstance(oid, ObjectId):
        raise AssertionError("ObjectId returned failed.")
        
    doc = repo.get_report(oid)
    if not doc:
        raise AssertionError("Report exists in MongoDB failed.")
        
    if doc.get("category") != expected_category:
        raise AssertionError(f"Correct category failed: expected {expected_category}, got {doc.get('category')}.")
        
    if doc.get("title") != expected_title:
        raise AssertionError(f"Correct title failed: expected {expected_title}, got {doc.get('title')}.")
        
    if not doc.get("content"):
        raise AssertionError("Report content not empty failed.")
        
    if not doc.get("metadata") or "generated_by" not in doc.get("metadata"):
        raise AssertionError("Metadata stored failed.")


def test_executive_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Executive Summary": "Strong Q2 performance across all regions.",
        "Key Metrics": {"Revenue": "$1M", "Growth": "15%"},
        "Business Highlights": ["Launched new product", "Expanded to EU"],
        "Business Risks": ["Supply chain delays"],
        "Recommended Actions": ["Increase marketing budget"]
    }
    oid = generator.generate_executive_report(data)
    verify_report(repo, oid, "executive", "Executive Dashboard")


def test_forecast_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Forecast Summary": "Growth expected to continue.",
        "Weekly Forecast": {"Week 1": "$200K"},
        "Monthly Forecast": {"July": "$800K"},
        "Quarterly Forecast": {"Q3": "$2.5M"},
        "Yearly Forecast": {"2026": "$10M"},
        "Growth Trend": "Upward",
        "Recommendations": "Maintain current strategy"
    }
    oid = generator.generate_forecast_report(data)
    verify_report(repo, oid, "forecast", "Forecast Report")


def test_marketing_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Marketing Performance": "Excellent",
        "Channel Contribution": {"Google Ads": "50%", "Facebook": "30%", "Organic": "20%"},
        "Campaign Performance": "Summer Sale was a hit.",
        "Budget Allocation": {"Google Ads": "$50K", "Facebook": "$30K"},
        "ROI": "2.5",
        "ROAS": "3.0",
        "Recommendations": "Shift budget to Google Ads."
    }
    oid = generator.generate_marketing_report(data)
    verify_report(repo, oid, "marketing", "Marketing Performance Report")


def test_sales_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Revenue": "$1,000,000",
        "Profit": "$250,000",
        "Growth": "12%",
        "Top Products": ["Product A", "Product B"],
        "Bottom Products": ["Product C"],
        "Sales Trends": "Increasing online sales.",
        "Recommendations": "Focus on Product A."
    }
    oid = generator.generate_sales_report(data)
    verify_report(repo, oid, "sales", "Sales Report")


def test_customer_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Customer Overview": "Growing user base.",
        "Segments": {"Enterprise": 20, "SMB": 80},
        "Retention": "95%",
        "Churn": "5%",
        "Average Order Value": "$500",
        "Lifetime Value": "$5000",
        "Recommendations": "Improve onboarding for SMB."
    }
    oid = generator.generate_customer_report(data)
    verify_report(repo, oid, "customer", "Customer Analytics Report")


def test_sentiment_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Sentiment Overview": "Mostly positive.",
        "Positive": "70%",
        "Neutral": "20%",
        "Negative": "10%",
        "Top Customer Complaints": ["App is slow", "Hard to find settings"],
        "Top Customer Praises": ["Great customer service"],
        "Trending Topics": ["New features"],
        "Recommendations": "Fix app speed."
    }
    oid = generator.generate_sentiment_report(data)
    verify_report(repo, oid, "sentiment", "Customer Sentiment Report")


def test_risk_report(generator: ReportGenerator, repo: ReportRepository) -> None:
    data = {
        "Business Risks": "Competitor launching similar product.",
        "Marketing Risks": "Ad costs rising.",
        "Sales Risks": "Key accounts up for renewal.",
        "Customer Risks": "High churn in specific segment.",
        "Risk Level": "Medium",
        "Mitigation Strategies": ["Offer discounts to key accounts", "Optimize ads"]
    }
    oid = generator.generate_risk_report(data)
    verify_report(repo, oid, "risk", "Risk Analysis Report")


def test_generate_all_reports(generator: ReportGenerator, repo: ReportRepository) -> None:
    repo.delete_all_reports()
    
    reports_data = {
        "executive": {"Executive Summary": "Exec content"},
        "forecast": {"Forecast Summary": "Forecast content"},
        "marketing": {"Marketing Performance": "Marketing content"},
        "sales": {"Revenue": "$100"},
        "customer": {"Customer Overview": "Customer content"},
        "sentiment": {"Sentiment Overview": "Sentiment content"},
        "risk": {"Business Risks": "Risk content"}
    }
    
    results = generator.generate_all_reports(reports_data)
    
    if len(results) != 7:
        raise AssertionError(f"Expected 7 reports generated, got {len(results)}.")
        
    for cat, oid in results.items():
        if not isinstance(oid, ObjectId):
            raise AssertionError(f"ObjectId returned failed for {cat}.")
            
    count = repo.count_reports()
    if count != 7:
        raise AssertionError(f"Every report inserted failed. Expected 7, got {count}.")


def test_empty_dictionary_validation(generator: ReportGenerator, repo: ReportRepository) -> None:
    try:
        generator.generate_executive_report({})
        raise AssertionError("Empty input did not raise exception.")
    except ValueError:
        pass


def test_invalid_input_validation(generator: ReportGenerator, repo: ReportRepository) -> None:
    invalid_inputs = [None, 123, [], "abc"]
    for i in invalid_inputs:
        try:
            generator.generate_executive_report(i)
            raise AssertionError(f"Invalid input {i} did not raise exception.")
        except TypeError:
            pass


def main():
    print("=" * 50)
    print("ReportGenerator Integration Tests")
    print("=" * 50)

    repo = ReportRepository()
    generator = ReportGenerator(repository=repo)
    
    # Test Isolation: Delete every document before running tests
    repo.delete_all_reports()
    
    tests = [
        ("Executive Report Test", test_executive_report),
        ("Forecast Report Test", test_forecast_report),
        ("Marketing Report Test", test_marketing_report),
        ("Sales Report Test", test_sales_report),
        ("Customer Report Test", test_customer_report),
        ("Sentiment Report Test", test_sentiment_report),
        ("Risk Report Test", test_risk_report),
        ("Generate All Reports Test", test_generate_all_reports),
        ("Empty Dictionary Validation Test", test_empty_dictionary_validation),
        ("Invalid Input Validation Test", test_invalid_input_validation)
    ]

    tests_passed = 0
    tests_failed = 0

    for name, func in tests:
        print_header(name)
        try:
            func(generator, repo)
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
