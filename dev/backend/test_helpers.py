from db import insert_job, update_job_status
from blob import upload_file
import time

def run_test():
    print("Starting test...")

    # Step 1: Insert job
    job_id = insert_job("TEST")
    print(f"Inserted job with ID: {job_id}")

    # Step 2: Update status → running
    update_job_status(job_id, "running")
    print("Updated status to running")

    # Step 3: Upload dummy report
    dummy_content = "# Test Report\n\nThis is a dummy report."
    url = upload_file("test_report.md", dummy_content)
    print(f"Uploaded report to: {url}")

    # Step 4: Update status → completed
    update_job_status(job_id, "completed")
    print("Updated status to completed")

    print("Test completed successfully")


if __name__ == "__main__":
    run_test()