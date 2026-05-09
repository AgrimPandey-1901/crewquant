from fastapi import FastAPI, Query, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dev.backend.helpers.db import insert_job, update_job_status, list_reports, get_report_by_job_id
from typing import List
from pydantic import BaseModel
from dev.backend.schemas.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    ReportResponse,
    ReportsListResponse,
    ErrorResponse
)
import time

# ---------------------------
# App Initialization
# ---------------------------
app = FastAPI(
    title="Multi-Agent Quant API",
    version="1.0.0"
)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code = 404,
        content = {
            "error":{
                "code": 404,
                "message": "Resource not found"
            }
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error"
            }
        }
    )

# ---------------------------
# CORS (for Streamlit later)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Health Check
# ---------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------
# Root Endpoint
# ---------------------------
@app.get("/")
def root():
    return {"message": "Quant API is running"}

def run_analysis_pipeline(job_id: int, ticker: str):

    print(f"Starting analysis for {ticker}")

    # mark running
    update_job_status(job_id, "running")

    # simulate long-running task
    time.sleep(5)

    # mark completed
    update_job_status(job_id, "completed")

    print(f"Completed analysis for {ticker}")

app = FastAPI()


@app.get("/reports", response_model=ReportsListResponse)
def get_reports(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    reports = list_reports(limit=limit, offset=offset)
    return ReportsListResponse(reports= reports)

@app.get("/reports/{job_id}", response_model=ReportResponse)
def get_report(job_id: str):
    report = get_report_by_job_id(job_id)

    if not report:
        raise HTTPException(
        status_code=404,
        detail={
            "code": 404,
            "message": "Report not found"
        }
    )

    return ReportResponse(**report)

@app.post("/analyze", response_model = AnalyzeResponse)
def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    ticker = request.ticker.upper().strip()

    job_id = insert_job("ticker")
    # run_agents(job_id)
    background_tasks.add_task(
        run_analysis_pipeline,
        job_id,
        ticker
    )
    return AnalyzeResponse(
        message= "Analysis job created",
        job_id= job_id,
        ticker= ticker,
        status= "pending"
    )