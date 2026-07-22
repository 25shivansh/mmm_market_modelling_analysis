"""
ReportImporter Module

Responsible for importing generated report files (.txt and .csv) into MongoDB
using the ReportRepository layer.
"""

import csv
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.database.report_repository import ReportRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportImporter:
    """
    Importer for reading generated report files from disk and saving them into MongoDB.
    """

    CATEGORIES = [
        "business",
        "forecast",
        "marketing",
        "recommendations",
        "sentiment",
        "customer",
        "sales",
    ]

    def __init__(self, repo: Optional[ReportRepository] = None):
        """
        Initialize ReportImporter.

        Args:
            repo (Optional[ReportRepository]): ReportRepository instance. Defaults to None.
        """
        try:
            self.repo = repo or ReportRepository()
            logger.info("ReportImporter initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ReportImporter: {e}")
            raise RuntimeError(f"Initialization error: {e}")

    def _infer_category(self, filename: str) -> str:
        """
        Infer document category from filename.

        Args:
            filename (str): Name of the file.

        Returns:
            str: Inferred category or 'general'.
        """
        filename_lower = filename.lower()
        for cat in self.CATEGORIES:
            if cat in filename_lower:
                return cat
        return "general"

    def _format_title(self, filename: str) -> str:
        """
        Format filename into a clean title.

        Args:
            filename (str): Name of the file.

        Returns:
            str: Clean title.
        """
        stem = Path(filename).stem
        title = stem.replace("_", " ").replace("-", " ").strip().title()
        return title if title else stem

    def _get_existing_filenames(self) -> set:
        """
        Fetch set of filenames already stored in the repository.

        Returns:
            set: Existing filenames.
        """
        try:
            reports = self.repo.get_reports()
            filenames = set()
            for r in reports:
                meta = r.get("metadata")
                if isinstance(meta, dict) and "filename" in meta:
                    filenames.add(meta["filename"])
            return filenames
        except Exception as e:
            logger.warning(f"Could not fetch existing reports: {e}")
            return set()

    def _process_txt_file(self, filepath: Path) -> tuple[str, Dict[str, Any]]:
        """
        Read and format content and metadata for a .txt file.

        Args:
            filepath (Path): Path to the .txt file.

        Returns:
            tuple[str, Dict[str, Any]]: (content, metadata)
        """
        content = filepath.read_text(encoding="utf-8")
        if not content or not content.strip():
            content = f"Report contents for {filepath.name}."
        metadata = {
            "filename": filepath.name,
            "file_type": "txt",
            "imported_at": datetime.now(timezone.utc).isoformat(),
        }
        return content, metadata

    def _process_csv_file(self, filepath: Path) -> tuple[str, Dict[str, Any]]:
        """
        Read and format summary content and metadata for a .csv file.

        Args:
            filepath (Path): Path to the .csv file.

        Returns:
            tuple[str, Dict[str, Any]]: (content, metadata)
        """
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            rows = list(reader)

        total_rows = len(rows)
        sample_rows = rows[:10]

        header_str = ", ".join(header) if header else "None"
        sample_rows_str = "\n".join([", ".join(r) for r in sample_rows]) if sample_rows else "None"

        content = (
            f"Column Names:\n{header_str}\n\n"
            f"Total Rows:\n{total_rows}\n\n"
            f"Sample Records:\n{sample_rows_str}"
        )

        metadata = {
            "filename": filepath.name,
            "file_type": "csv",
            "rows": total_rows,
            "columns": len(header) if header else 0,
            "imported_at": datetime.now(timezone.utc).isoformat(),
        }
        return content, metadata

    def import_report(self, filepath: Union[str, Path]) -> Optional[str]:
        """
        Import a single report file into MongoDB.

        Args:
            filepath (Union[str, Path]): Path to the report file.

        Returns:
            Optional[str]: Inserted report ID string if successful, None if skipped or unsupported.

        Raises:
            ValueError: If filepath is None, invalid, or file does not exist.
        """
        if filepath is None:
            raise ValueError("filepath cannot be None.")
        if not isinstance(filepath, (str, Path)):
            raise ValueError("filepath must be a string or Path object.")

        path = Path(filepath)
        if not path.exists() or not path.is_file():
            raise ValueError(f"File does not exist: {filepath}")

        ext = path.suffix.lower()
        if ext not in [".txt", ".csv"]:
            logger.info(f"Skipped unsupported file type: {path.name}")
            return None

        # Check for duplicate
        existing = self._get_existing_filenames()
        if path.name in existing:
            logger.info(f"Skipped: {path.name} (already exists)")
            return None

        title = self._format_title(path.name)
        category = self._infer_category(path.name)

        try:
            if ext == ".txt":
                content, metadata = self._process_txt_file(path)
            else:
                content, metadata = self._process_csv_file(path)

            report_id = self.repo.save_report(
                category=category,
                title=title,
                content=content,
                metadata=metadata,
            )
            logger.info(f"Imported: {path.name}")
            return str(report_id)

        except Exception as e:
            logger.error(f"Failed: {path.name} ({e})")
            raise RuntimeError(f"Error importing file {path.name}: {e}")

    def import_reports(self, directory: Union[str, Path]) -> int:
        """
        Import all supported report files (.txt, .csv) in a directory.

        Args:
            directory (Union[str, Path]): Path to directory containing report files.

        Returns:
            int: Number of successfully imported reports.

        Raises:
            ValueError: If directory is None, invalid, or does not exist.
        """
        if directory is None:
            raise ValueError("directory cannot be None.")
        if not isinstance(directory, (str, Path)):
            raise ValueError("directory must be a string or Path object.")

        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"Directory does not exist: {directory}")

        imported_count = 0
        skipped_count = 0
        failed_count = 0

        # Collect existing filenames once for efficiency
        existing_filenames = self._get_existing_filenames()

        file_paths = sorted([p for p in dir_path.iterdir() if p.is_file()])

        for path in file_paths:
            ext = path.suffix.lower()
            if ext not in [".txt", ".csv"]:
                continue

            if path.name in existing_filenames:
                logger.info(f"Skipped: {path.name}")
                skipped_count += 1
                continue

            try:
                res = self.import_report(path)
                if res:
                    imported_count += 1
                    existing_filenames.add(path.name)
                else:
                    skipped_count += 1
            except Exception as e:
                logger.error(f"Failed: {path.name} ({e})")
                failed_count += 1

        logger.info(f"Imported: {imported_count}")
        logger.info(f"Skipped: {skipped_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Total imported: {imported_count}")

        return imported_count
