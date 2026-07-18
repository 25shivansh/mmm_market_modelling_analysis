from typing import Dict, Any, Optional
from bson.objectid import ObjectId

from src.database.report_repository import ReportRepository
from src.knowledge_reports.report_templates import ReportTemplates


class ReportGenerator:
    """Orchestration layer for generating and storing business reports."""

    def __init__(self, repository: Optional[ReportRepository] = None) -> None:
        """
        Initializes the ReportGenerator.

        Args:
            repository (ReportRepository, optional): An instance of ReportRepository.
                If not provided, a new instance will be created.
        """
        self._repository = repository or ReportRepository()

    def _validate_data(self, data: Any) -> Dict[str, Any]:
        """
        Validates that the provided data is a non-empty dictionary.

        Args:
            data: The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If data is an empty dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError(f"Data must be a dictionary, got {type(data).__name__}.")
        if not data:
            raise ValueError("Data dictionary cannot be empty.")
        return data

    def _generate_and_save(
        self, 
        data: Dict[str, Any], 
        category: str, 
        title: str, 
        template_func
    ) -> ObjectId:
        """
        Internal helper to validate data, format the report, and save it.

        Args:
            data (dict): The report data.
            category (str): The report category.
            title (str): The report title.
            template_func (callable): The formatting function from ReportTemplates.

        Returns:
            ObjectId: The ID of the inserted report.
        """
        valid_data = self._validate_data(data)
        
        # Inject the title into the data so the template can use it
        if "Title" not in valid_data:
            valid_data["Title"] = title

        content = template_func(valid_data)
        
        return self._repository.save_report(
            category=category,
            title=title,
            content=content,
            metadata={"generated_by": "ReportGenerator"}
        )

    def generate_executive_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves an Executive Dashboard report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="executive", 
            title="Executive Dashboard", 
            template_func=ReportTemplates.executive_dashboard
        )

    def generate_forecast_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves a Forecast Report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="forecast", 
            title="Forecast Report", 
            template_func=ReportTemplates.forecast_report
        )

    def generate_marketing_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves a Marketing Performance Report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="marketing", 
            title="Marketing Performance Report", 
            template_func=ReportTemplates.marketing_report
        )

    def generate_sales_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves a Sales Report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="sales", 
            title="Sales Report", 
            template_func=ReportTemplates.sales_report
        )

    def generate_customer_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves a Customer Analytics Report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="customer", 
            title="Customer Analytics Report", 
            template_func=ReportTemplates.customer_report
        )

    def generate_sentiment_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves a Customer Sentiment Report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="sentiment", 
            title="Customer Sentiment Report", 
            template_func=ReportTemplates.sentiment_report
        )

    def generate_risk_report(self, data: Dict[str, Any]) -> ObjectId:
        """
        Generates and saves a Risk Analysis Report.

        Args:
            data (dict): The data for the report.

        Returns:
            ObjectId: The ID of the saved report.
        """
        return self._generate_and_save(
            data, 
            category="risk", 
            title="Risk Analysis Report", 
            template_func=ReportTemplates.risk_report
        )

    def generate_all_reports(self, reports: Dict[str, Dict[str, Any]]) -> Dict[str, ObjectId]:
        """
        Generates all provided reports by delegating to specific methods.

        Args:
            reports (dict): A dictionary mapping categories to their report data.

        Returns:
            dict: A mapping of category names to their inserted ObjectIds.
            
        Raises:
            TypeError: If the input is not a dictionary.
            ValueError: If the input is empty.
        """
        if not isinstance(reports, dict):
            raise TypeError(f"Reports must be a dictionary, got {type(reports).__name__}.")
        if not reports:
            raise ValueError("Reports dictionary cannot be empty.")

        method_map = {
            "executive": self.generate_executive_report,
            "forecast": self.generate_forecast_report,
            "marketing": self.generate_marketing_report,
            "sales": self.generate_sales_report,
            "customer": self.generate_customer_report,
            "sentiment": self.generate_sentiment_report,
            "risk": self.generate_risk_report,
        }

        results = {}
        for category, data in reports.items():
            if category in method_map:
                results[category] = method_map[category](data)
        
        return results
