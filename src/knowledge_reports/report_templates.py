from typing import Dict, Any, List

class ReportTemplates:
    """Provides reusable formatting templates for business reports."""

    @staticmethod
    def _format_header(title: str) -> str:
        """Formats the main report header."""
        border = "=" * 60
        title_str = title if title else "N/A"
        return f"{border}\n{title_str}\n{border}\n\n"

    @staticmethod
    def _format_footer() -> str:
        """Formats the main report footer."""
        return "\n\n" + "=" * 60 + "\n"

    @staticmethod
    def _format_separator() -> str:
        """Formats a section separator."""
        return "\n\n" + "-" * 60 + "\n\n"

    @staticmethod
    def _format_key_value(key: str, value: Any) -> str:
        """Formats a single key-value pair."""
        val = str(value) if value is not None and value != "" else "N/A"
        return f"{key} : {val}"

    @staticmethod
    def _format_list(items: List[Any]) -> str:
        """Formats a list of items."""
        if not items:
            return "N/A"
        return "\n".join([f"- {str(item) if item is not None and item != '' else 'N/A'}" for item in items])

    @staticmethod
    def _format_section(title: str, content: Any) -> str:
        """Formats an individual report section."""
        result = f"{title}\n\n"
        if content is None or content == "":
            result += "N/A"
        elif isinstance(content, dict):
            items = []
            for k, v in content.items():
                items.append(ReportTemplates._format_key_value(str(k), v))
            result += "\n\n".join(items)
        elif isinstance(content, list):
            result += ReportTemplates._format_list(content)
        else:
            result += str(content)
        return result

    @staticmethod
    def _build_report(data: Dict[str, Any], sections: List[str]) -> str:
        """Constructs the full report based on provided data and requested sections."""
        title = data.get("Title", "Untitled Report")
        report = ReportTemplates._format_header(title)
        
        section_blocks = []
        for sec in sections:
            if sec not in ["Title", "Generated Timestamp"]:
                section_blocks.append(ReportTemplates._format_section(sec, data.get(sec)))
                
        if section_blocks:
            report += ReportTemplates._format_separator().join(section_blocks)
            
        report += ReportTemplates._format_footer()
        
        if "Generated Timestamp" in sections:
            timestamp = data.get("Generated Timestamp", "N/A")
            report += f"\nGenerated Timestamp: {timestamp}\n"
            
        return report

    @staticmethod
    def executive_dashboard(data: Dict[str, Any]) -> str:
        """Generates an Executive Dashboard report."""
        sections = [
            "Title",
            "Executive Summary",
            "Key Metrics",
            "Business Highlights",
            "Business Risks",
            "Recommended Actions",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)

    @staticmethod
    def forecast_report(data: Dict[str, Any]) -> str:
        """Generates a Forecast report."""
        sections = [
            "Title",
            "Forecast Summary",
            "Weekly Forecast",
            "Monthly Forecast",
            "Quarterly Forecast",
            "Yearly Forecast",
            "Growth Trend",
            "Recommendations",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)

    @staticmethod
    def marketing_report(data: Dict[str, Any]) -> str:
        """Generates a Marketing report."""
        sections = [
            "Title",
            "Marketing Performance",
            "Channel Contribution",
            "Campaign Performance",
            "Budget Allocation",
            "ROI",
            "ROAS",
            "Recommendations",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)

    @staticmethod
    def sales_report(data: Dict[str, Any]) -> str:
        """Generates a Sales report."""
        sections = [
            "Title",
            "Revenue",
            "Profit",
            "Growth",
            "Top Products",
            "Bottom Products",
            "Sales Trends",
            "Recommendations",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)

    @staticmethod
    def customer_report(data: Dict[str, Any]) -> str:
        """Generates a Customer report."""
        sections = [
            "Title",
            "Customer Overview",
            "Segments",
            "Retention",
            "Churn",
            "Average Order Value",
            "Lifetime Value",
            "Recommendations",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)

    @staticmethod
    def sentiment_report(data: Dict[str, Any]) -> str:
        """Generates a Sentiment report."""
        sections = [
            "Title",
            "Sentiment Overview",
            "Positive",
            "Neutral",
            "Negative",
            "Top Customer Complaints",
            "Top Customer Praises",
            "Trending Topics",
            "Recommendations",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)

    @staticmethod
    def risk_report(data: Dict[str, Any]) -> str:
        """Generates a Risk report."""
        sections = [
            "Title",
            "Business Risks",
            "Marketing Risks",
            "Sales Risks",
            "Customer Risks",
            "Risk Level",
            "Mitigation Strategies",
            "Generated Timestamp"
        ]
        return ReportTemplates._build_report(data, sections)
