import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class ConfigError(Exception):
    pass


def get_env_variable(name: str, required: bool = True, default=None):
    value = os.getenv(name, default)

    if required and (value is None or value.strip() == ""):
        raise ConfigError(f"Missing required environment variable: {name}")

    return value


# ---------------------------
# Database Config
# ---------------------------
DB_HOST = get_env_variable("DB_HOST")
DB_NAME = get_env_variable("DB_NAME")
DB_USER = get_env_variable("DB_USER")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_PORT = int(get_env_variable("DB_PORT", default=5432))


# ---------------------------
# Azure Blob Config
# ---------------------------
BLOB_CONNECTION_STRING = get_env_variable("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = get_env_variable("BLOB_CONTAINER_NAME", default="reports")


# ---------------------------
# LLM Config (optional)
# ---------------------------
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY", required=False)


# ---------------------------
# Validation Checks
# ---------------------------
def validate_config():
    # Basic DB validation
    if "postgres" not in DB_HOST:
        raise ConfigError("DB_HOST does not look like a valid PostgreSQL host")

    # Azure connection string validation
    if "AccountName" not in BLOB_CONNECTION_STRING:
        raise ConfigError("Invalid Azure Storage connection string")

    print("✅ Config validation passed")


# Run validation at import time (optional but recommended for this project)
validate_config()