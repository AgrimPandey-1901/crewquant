import os
import psycopg2
from contextlib import contextmanager
from datetime import datetime
from dotenv import load_dotenv
from dev.backend.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

load_dotenv()

DB_CONFIG = {
    "host":DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "sslmode": "require"
}

# ---------------------------
# Connection Manager
# ---------------------------
@contextmanager
def connect():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    finally:
        if conn:
            conn.close()


# ---------------------------
# Insert Job
# ---------------------------
def insert_job(ticker: str, status: str = "pending") -> int:
    query = """
        INSERT INTO analysis_jobs (ticker, status)
        VALUES (%s, %s)
        RETURNING id;
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (ticker, status))
            job_id = cur.fetchone()[0]
            conn.commit()

    return job_id


# ---------------------------
# Update Job Status
# ---------------------------
def update_job_status(job_id: int, status: str):
    query = """
        UPDATE analysis_jobs
        SET status = %s,
            created_at = %s
        WHERE id = %s;
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (status, datetime.now(), job_id))
            conn.commit()
# -----------------------------------
# Fetch latest n reports
# -----------------------------------
def list_reports(limit: int = 10, offset: int = 0):
    query = """
        SELECT id, job_id, blob_url, summary, created_at
        FROM reports
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s;
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit, offset))
            rows = cur.fetchall()

    # convert tuples → dicts
    reports = []
    for row in rows:
        reports.append({
            "id": row[0],
            "job_id": row[1],
            "blob_url": row[2],
            "summary": row[3],
            "created_at": row[4].isoformat() if row[4] else None
        })

    return reports

# -----------------------------------------
# Fetch a single report from db
# -----------------------------------------
def get_report_by_job_id(job_id: str):
    query = """
        SELECT id, job_id, blob_url, created_at
        FROM reports
        WHERE job_id = %s;
    """

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (job_id,))
            row = cur.fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "job_id": row[1],
        "blob_url": row[2],
        "created_at": row[3].isoformat() if row[3] else None
    }
