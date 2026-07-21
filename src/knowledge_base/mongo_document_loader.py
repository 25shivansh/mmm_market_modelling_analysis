"""
MongoDocumentLoader loads reports from MongoDB and converts them to LangChain Documents.
"""

from langchain_core.documents import Document

from src.database.report_repository import ReportRepository


class MongoDocumentLoader:
    """Loader for converting MongoDB report documents into LangChain Document objects."""

    def __init__(self, repository=None):
        self.repository = repository or ReportRepository()

    def _validate_string(self, value, param_name):
        if not isinstance(value, str):
            raise ValueError(f"{param_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{param_name} cannot be empty.")
        return value.strip()

    def load_all_documents(self):
        """Fetch all reports from MongoDB and convert them into LangChain Documents."""
        reports = self.repository.get_reports()
        if not reports:
            return []
        return [self.to_document(report) for report in reports]

    def load_documents_by_category(self, category):
        """Fetch reports of a specific category and convert them into LangChain Documents."""
        category = self._validate_string(category, "category")
        reports = self.repository.get_reports_by_category(category)
        if not reports:
            return []
        return [self.to_document(report) for report in reports]

    def load_document(self, report_id):
        """Fetch a single report by ID and convert it into a LangChain Document."""
        report_id = self._validate_string(report_id, "report_id")
        report = self.repository.get_report(report_id)
        if not report:
            return None
        return self.to_document(report)

    def count_documents(self):
        """Return the total number of reports stored in MongoDB."""
        return self.repository.count_reports()

    def to_document(self, report):
        """Convert a report document dictionary into a LangChain Document object."""
        if not report or not isinstance(report, dict):
            raise ValueError("report must be a non-empty dictionary.")

        extra_metadata = report.get("metadata")
        if isinstance(extra_metadata, dict):
            metadata = dict(extra_metadata)
        else:
            metadata = {}

        created_at = report.get("created_at")
        updated_at = report.get("updated_at")

        created_at_str = created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at)
        updated_at_str = updated_at.isoformat() if hasattr(updated_at, "isoformat") else str(updated_at)

        metadata.update({
            "report_id": str(report["_id"]),
            "category": report["category"],
            "title": report["title"],
            "created_at": created_at_str,
            "updated_at": updated_at_str
        })

        return Document(
            page_content=report["content"],
            metadata=metadata
        )
