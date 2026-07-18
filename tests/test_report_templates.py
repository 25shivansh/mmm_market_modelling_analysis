import os
import sys
import traceback
from datetime import datetime

# Adjust the path to make sure src is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.knowledge_reports.report_templates import ReportTemplates

class TestRunner:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0

    def run_test(self, name, test_func):
        self.total += 1
        print("-" * 50)
        print(f"Running {name}")
        print("-" * 50)
        try:
            test_func()
            print("\nPASS\n")
            self.passed += 1
        except AssertionError as e:
            print(f"\nFAIL: {e}\n")
            self.failed += 1
        except Exception as e:
            print(f"\nFAIL: Unexpected error: {traceback.format_exc()}\n")
            self.failed += 1

def assert_common_report_checks(report, title, expected_sections):
    assert isinstance(report, str), "Return type should be str"
    assert len(report.strip()) > 0, "Report should not be empty"
    assert title in report, f"Correct title '{title}' missing in report"
    for section in expected_sections:
        assert section in report, f"Expected section '{section}' missing in report"
    assert "Generated Timestamp" in report, "Timestamp section missing"

def test_executive_dashboard():
    data = {
        "Title": "Executive Summary Q3",
        "Executive Summary": "Strong performance across all business units.",
        "Key Metrics": {"Revenue": "$1.2M", "Growth": "15%", "EBITDA": "$300K"},
        "Business Highlights": ["Launched new AI product", "Expanded to EMEA region"],
        "Business Risks": ["Supply chain delays", "Competitor price cuts"],
        "Recommended Actions": ["Accelerate marketing spend in EMEA", "Diversify suppliers"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.executive_dashboard(data)
    sections = [
        "Executive Summary",
        "Key Metrics",
        "Business Highlights",
        "Business Risks",
        "Recommended Actions"
    ]
    assert_common_report_checks(report, "Executive Summary Q3", sections)

def test_forecast_report():
    data = {
        "Title": "Q4 Sales Forecast",
        "Forecast Summary": "Expecting 20% YoY growth.",
        "Weekly Forecast": {"Week 1": "$50K", "Week 2": "$55K"},
        "Monthly Forecast": {"October": "$200K", "November": "$250K", "December": "$300K"},
        "Quarterly Forecast": {"Q4": "$750K"},
        "Yearly Forecast": {"2024": "$2.5M"},
        "Growth Trend": "Upward trajectory",
        "Recommendations": ["Ensure inventory is stocked for Dec"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.forecast_report(data)
    sections = [
        "Forecast Summary",
        "Weekly Forecast",
        "Monthly Forecast",
        "Quarterly Forecast",
        "Yearly Forecast",
        "Growth Trend",
        "Recommendations"
    ]
    assert_common_report_checks(report, "Q4 Sales Forecast", sections)

def test_marketing_report():
    data = {
        "Title": "Q3 Marketing ROI",
        "Marketing Performance": "Exceeded leads target by 10%.",
        "Channel Contribution": {"Google Ads": "40%", "Facebook": "30%", "LinkedIn": "20%", "Email": "10%"},
        "Campaign Performance": {"Summer Sale": "Excellent", "Back to School": "Good"},
        "Budget Allocation": {"Google Ads": "$40K", "Facebook": "$30K"},
        "ROI": "150%",
        "ROAS": "2.5x",
        "Recommendations": ["Shift $10K from Facebook to Google Ads"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.marketing_report(data)
    sections = [
        "Marketing Performance",
        "Channel Contribution",
        "Campaign Performance",
        "Budget Allocation",
        "ROI",
        "ROAS",
        "Recommendations"
    ]
    assert_common_report_checks(report, "Q3 Marketing ROI", sections)

def test_sales_report():
    data = {
        "Title": "Annual Sales Report",
        "Revenue": "$5.0M",
        "Profit": "$1.2M",
        "Growth": "25% YoY",
        "Top Products": ["Product A", "Product B"],
        "Bottom Products": ["Product X", "Product Y"],
        "Sales Trends": "Seasonality observed in Q2",
        "Recommendations": ["Discontinue Product Y", "Increase stock for Product A"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.sales_report(data)
    sections = [
        "Revenue",
        "Profit",
        "Growth",
        "Top Products",
        "Bottom Products",
        "Sales Trends",
        "Recommendations"
    ]
    assert_common_report_checks(report, "Annual Sales Report", sections)

def test_customer_report():
    data = {
        "Title": "Customer Health Metrics",
        "Customer Overview": "Total active users increased to 10K.",
        "Segments": {"Enterprise": "20%", "SMB": "50%", "Individual": "30%"},
        "Retention": "85%",
        "Churn": "15%",
        "Average Order Value": "$120",
        "Lifetime Value": "$1,200",
        "Recommendations": ["Implement loyalty program for SMB segment"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.customer_report(data)
    sections = [
        "Customer Overview",
        "Segments",
        "Retention",
        "Churn",
        "Average Order Value",
        "Lifetime Value",
        "Recommendations"
    ]
    assert_common_report_checks(report, "Customer Health Metrics", sections)

def test_sentiment_report():
    data = {
        "Title": "Brand Sentiment Analysis",
        "Sentiment Overview": "Overall sentiment is largely positive.",
        "Positive": "65%",
        "Neutral": "20%",
        "Negative": "15%",
        "Top Customer Complaints": ["Shipping delays", "App crashes"],
        "Top Customer Praises": ["Great customer service", "Easy to use UI"],
        "Trending Topics": ["New feature launch", "Holiday discount"],
        "Recommendations": ["Investigate app stability issues"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.sentiment_report(data)
    sections = [
        "Sentiment Overview",
        "Positive",
        "Neutral",
        "Negative",
        "Top Customer Complaints",
        "Top Customer Praises",
        "Trending Topics",
        "Recommendations"
    ]
    assert_common_report_checks(report, "Brand Sentiment Analysis", sections)

def test_risk_report():
    data = {
        "Title": "Enterprise Risk Assessment",
        "Business Risks": ["Economic downturn", "Regulatory changes"],
        "Marketing Risks": ["Increased CPC", "Data privacy laws"],
        "Sales Risks": ["High dependency on top 3 clients"],
        "Customer Risks": ["Rising churn in SMB segment"],
        "Risk Level": "Medium",
        "Mitigation Strategies": ["Diversify client base", "Optimize ad spend"],
        "Generated Timestamp": datetime.now().isoformat()
    }
    report = ReportTemplates.risk_report(data)
    sections = [
        "Business Risks",
        "Marketing Risks",
        "Sales Risks",
        "Customer Risks",
        "Risk Level",
        "Mitigation Strategies"
    ]
    assert_common_report_checks(report, "Enterprise Risk Assessment", sections)

def test_empty_dictionary():
    reports = [
        ReportTemplates.executive_dashboard,
        ReportTemplates.forecast_report,
        ReportTemplates.marketing_report,
        ReportTemplates.sales_report,
        ReportTemplates.customer_report,
        ReportTemplates.sentiment_report,
        ReportTemplates.risk_report
    ]
    for r_func in reports:
        report = r_func({})
        assert isinstance(report, str), "Return type should be str"
        assert len(report.strip()) > 0, "Report should not be empty"
        assert "N/A" in report, "Missing values should be rendered as N/A"

def test_missing_keys():
    data = {
        "Executive Summary": "Revenue increased."
    }
    report = ReportTemplates.executive_dashboard(data)
    assert "Revenue increased." in report, "Provided key should be in report"
    assert "N/A" in report, "Missing fields should become N/A"
    assert report.count("N/A") > 2, "There should be multiple N/As for missing keys"

def test_list_formatting():
    data = {
        "Recommended Actions": [
            "Increase Google Ads budget",
            "Improve customer retention",
            "Reduce Facebook spend"
        ]
    }
    report = ReportTemplates.executive_dashboard(data)
    assert "- Increase Google Ads budget" in report, "List item 1 missing"
    assert "- Improve customer retention" in report, "List item 2 missing"
    assert "- Reduce Facebook spend" in report, "List item 3 missing"

if __name__ == "__main__":
    print("==================================================")
    print("Testing ReportTemplates")
    print("==================================================\n")

    runner = TestRunner()
    
    runner.run_test("Executive Dashboard Test", test_executive_dashboard)
    runner.run_test("Forecast Report Test", test_forecast_report)
    runner.run_test("Marketing Report Test", test_marketing_report)
    runner.run_test("Sales Report Test", test_sales_report)
    runner.run_test("Customer Report Test", test_customer_report)
    runner.run_test("Sentiment Report Test", test_sentiment_report)
    runner.run_test("Risk Report Test", test_risk_report)
    runner.run_test("Empty Dictionary Handling Test", test_empty_dictionary)
    runner.run_test("Missing Keys Handling Test", test_missing_keys)
    runner.run_test("List Formatting Test", test_list_formatting)

    print("==================================================")
    print("Test Summary")
    print("==================================================")
    print(f"Total Tests : {runner.total}")
    print(f"Passed      : {runner.passed}")
    print(f"Failed      : {runner.failed}")
    print("==================================================")

    if runner.failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)
