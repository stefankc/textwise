import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """

    DATABASE_URL: str
    OPENAI_API_KEY: str
    FRONTEND_DIR: str
    # List of allowed origins for CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        """
        Configuration for environment variables.
        """
        env_file = ".env"  # File containing environment variables


# Project base directory
BASE_DIR = Path(__file__).resolve().parent

# Path to the frontend build directory
FRONTEND_DIR = (BASE_DIR / "../../frontend/build").resolve()
print(BASE_DIR)

# Check if the frontend build directory exists
if not FRONTEND_DIR.exists():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.error(f"Frontend build directory does not exist at {FRONTEND_DIR}")
    raise Exception(
        f"Frontend build directory does not exist at {FRONTEND_DIR}")

# Regex pattern for filename validation
# Allows letters, numbers, underscores, hyphens, dots, and spaces
FILENAME_REGEX = r"^[a-zA-Z0-9_\-\. ]+$"

# Temporary directory for file uploads
TEMP_DIR = BASE_DIR / "temp"
# Create the temp directory if it doesn't exist
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Optional: Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
