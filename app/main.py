import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Add project root directory to Python path so we can import from `src`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import existing AI module directly
from src.data_understanding import DataUnderstanding

app = FastAPI(
    title="MMM AI Engine API",
    description="FastAPI service exposing Market Mix Modeling & Dataset Analysis",
    version="1.0.0"
)

# Request schema from Express.js
class AnalyzeRequest(BaseModel):
    filePath: str
    datasetId: Optional[str] = None


@app.get("/")
def root():
    return {"status": "online", "message": "MMM AI Engine FastAPI is running"}


@app.post("/api/analyze")
def analyze_dataset(payload: AnalyzeRequest):
    """
    Analyzes a CSV file using the existing DataUnderstanding module
    and returns the generated summary report.
    """
    file_path = Path(payload.filePath)

    # Check if the file exists (checking absolute, project root, and backend subfolder)
    if not file_path.exists():
        if (PROJECT_ROOT / payload.filePath).exists():
            file_path = PROJECT_ROOT / payload.filePath
        elif (PROJECT_ROOT / "backend" / payload.filePath).exists():
            file_path = PROJECT_ROOT / "backend" / payload.filePath

    if not file_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"CSV file not found at path: {payload.filePath} (Resolved path: {file_path})"
        )

    try:
        # Initialize and run existing DataUnderstanding analyzer
        analyzer = DataUnderstanding(str(file_path))
        
        if analyzer.load_data() is None:
            raise HTTPException(status_code=400, detail="Failed to parse dataset CSV.")

        # Re-use existing method to generate full textual report
        report_content = analyzer.generate_full_report()
        
        # Get shape info
        rows, cols = analyzer.get_shape()

        return {
            "success": True,
            "message": "Analysis completed successfully",
            "datasetId": payload.datasetId,
            "summary": {
                "rows": rows,
                "columns": cols,
            },
            "reportContent": report_content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
