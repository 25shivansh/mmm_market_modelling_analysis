from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from bson.objectid import ObjectId
from pymongo.collection import Collection

from src.database.mongodb import MongoDBManager


class ReportRepository:
    """Repository layer for managing reports in MongoDB."""

    def __init__(self, db_manager: Optional[MongoDBManager] = None) -> None:
        """
        Initializes the ReportRepository.

        Args:
            db_manager (MongoDBManager, optional): An instance of MongoDBManager.
                If not provided, a new instance will be created.
        """
        self._db_manager = db_manager or MongoDBManager()
        self._db_manager.connect()
        self._collection: Collection = self._db_manager.get_collection("reports")

    def _validate_string(self, value: Any, field_name: str) -> str:
        """Validates that a value is a non-empty string."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string, got {type(value).__name__}.")
        value_stripped = value.strip()
        if not value_stripped:
            raise ValueError(f"{field_name} cannot be empty.")
        return value_stripped

    def _validate_object_id(self, report_id: Any) -> ObjectId:
        """Validates and converts a value to an ObjectId."""
        if isinstance(report_id, ObjectId):
            return report_id
        if not isinstance(report_id, str):
            raise TypeError(f"report_id must be a string or ObjectId, got {type(report_id).__name__}.")
        if not ObjectId.is_valid(report_id):
            raise ValueError(f"Invalid ObjectId format: {report_id}")
        return ObjectId(report_id)

    def _validate_metadata(self, metadata: Any) -> Dict[str, Any]:
        """Validates that metadata is a dictionary or None."""
        if metadata is None:
            return {}
        if not isinstance(metadata, dict):
            raise TypeError(f"metadata must be a dict, got {type(metadata).__name__}.")
        return metadata

    def save_report(
        self,
        category: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ObjectId:
        """
        Inserts a new report into the database.

        Args:
            category (str): The category of the report.
            title (str): The title of the report.
            content (str): The main content of the report.
            metadata (dict, optional): Additional metadata.

        Returns:
            ObjectId: The ID of the inserted report.

        Raises:
            TypeError: If argument types are invalid.
            ValueError: If required fields are empty.
        """
        category = self._validate_string(category, "category")
        title = self._validate_string(title, "title")
        content = self._validate_string(content, "content")
        metadata = self._validate_metadata(metadata)

        now = datetime.now(timezone.utc)
        
        document = {
            "category": category,
            "title": title,
            "content": content,
            "metadata": metadata,
            "created_at": now,
            "updated_at": now
        }

        result = self._collection.insert_one(document)
        return result.inserted_id

    def get_report(self, report_id: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single report by its ID.

        Args:
            report_id: The ID of the report.

        Returns:
            dict: The report document if found, else None.

        Raises:
            TypeError: If report_id has an invalid type.
            ValueError: If report_id has an invalid format.
        """
        oid = self._validate_object_id(report_id)
        return self._collection.find_one({"_id": oid})

    def get_reports(self) -> List[Dict[str, Any]]:
        """
        Retrieves all reports, ordered by newest first.

        Returns:
            list: A list of report documents.
        """
        cursor = self._collection.find().sort("created_at", -1)
        return list(cursor)

    def get_reports_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Retrieves all reports for a specific category, ordered by newest first.

        Args:
            category (str): The category to filter by.

        Returns:
            list: A list of report documents in the specified category.

        Raises:
            TypeError: If category is not a string.
            ValueError: If category is empty.
        """
        category = self._validate_string(category, "category")
        cursor = self._collection.find({"category": category}).sort("created_at", -1)
        return list(cursor)

    def update_report(
        self,
        report_id: Any,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Updates the content and/or metadata of an existing report.

        Args:
            report_id: The ID of the report to update.
            content (str): The new content.
            metadata (dict, optional): The new metadata.

        Returns:
            bool: True if the report was updated, False if it was not found.

        Raises:
            TypeError: If argument types are invalid.
            ValueError: If arguments have invalid values/formats.
        """
        oid = self._validate_object_id(report_id)
        content = self._validate_string(content, "content")
        metadata = self._validate_metadata(metadata)

        now = datetime.now(timezone.utc)
        
        update_data = {
            "content": content,
            "metadata": metadata,
            "updated_at": now
        }

        result = self._collection.update_one(
            {"_id": oid},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_report(self, report_id: Any) -> bool:
        """
        Deletes a report by its ID.

        Args:
            report_id: The ID of the report to delete.

        Returns:
            bool: True if the report was deleted, False if not found.

        Raises:
            TypeError: If report_id has an invalid type.
            ValueError: If report_id has an invalid format.
        """
        oid = self._validate_object_id(report_id)
        result = self._collection.delete_one({"_id": oid})
        return result.deleted_count > 0

    def delete_all_reports(self) -> int:
        """
        Deletes all reports in the collection.

        Returns:
            int: The number of reports deleted.
        """
        result = self._collection.delete_many({})
        return result.deleted_count

    def count_reports(self) -> int:
        """
        Counts the total number of reports in the collection.

        Returns:
            int: The total report count.
        """
        return self._collection.count_documents({})
