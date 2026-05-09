import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from dotenv import load_dotenv
from crewquant_repo.dev.backend.config import BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME

load_dotenv()

# Load config
CONNECTION_STRING = BLOB_CONNECTION_STRING
CONTAINER_NAME = BLOB_CONTAINER_NAME

# Create client once (singleton pattern)
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


# ---------------------------
# Upload File
# ---------------------------
def upload_file(filename: str, content: str) -> str:
    """
    Uploads content to Azure Blob Storage and returns the file URL.
    """

    # Optional: add timestamp to avoid collisions
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    blob_name = f"{timestamp}_{filename}"

    blob_client = container_client.get_blob_client(blob_name)

    # Upload (overwrite=False prevents accidental overwrite)
    blob_client.upload_blob(content, overwrite=False)

    # Return URL
    return blob_client.url