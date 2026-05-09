from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# -----------------------------------
# Analyze Request
# -----------------------------------
class AnalyzeRequest(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Stock ticker symbol"
    )


# -----------------------------------
# Analyze Response
# -----------------------------------
class AnalyzeResponse(BaseModel):
    message: str
    job_id: int
    ticker: str
    status: str


# -----------------------------------
# Report Model
# -----------------------------------
class ReportResponse(BaseModel):
    id: int
    job_id: int
    blob_url: str
    created_at: datetime


# -----------------------------------
# Reports List Response
# -----------------------------------
class ReportsListResponse(BaseModel):
    reports: List[ReportResponse]


# -----------------------------------
# Error Response (optional)
# -----------------------------------
class ErrorDetail(BaseModel):
    code: int
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail