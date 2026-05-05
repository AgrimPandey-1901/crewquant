import os
import psycopg2
from contextlib import contextmanager
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
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
