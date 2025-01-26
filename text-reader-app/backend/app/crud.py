"""
CRUD operations for managing API keys.

This module provides functions to read and write API keys to a configuration file.
"""

import json
from pathlib import Path
from typing import Optional
from .schemas import APIKeys
import logging

# Define the path to the configuration file
CONFIG_FILE = Path(__file__).parent / "config.json"


def read_api_keys() -> Optional[APIKeys]:
    """
    Read API keys from the configuration file.

    Returns:
        Optional[APIKeys]: An instance of APIKeys if the config file exists and is valid, otherwise None.
    """
    if not CONFIG_FILE.exists():
        logging.warning(f"Configuration file not found at {CONFIG_FILE}.")
        return None
    with open(CONFIG_FILE, "r") as f:
        try:
            data = json.load(f)
            logging.info(f"API keys successfully read from {CONFIG_FILE}.")
            return APIKeys(**data)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {CONFIG_FILE}: {e}")
            return None


def write_api_keys(api_keys: APIKeys) -> None:
    """
    Write API keys to the configuration file.

    Args:
        api_keys (APIKeys): An instance of APIKeys containing the keys to be saved.

    Raises:
        Exception: Propagates any exception that occurs during the file write operation.
    """
    try:
        # Ensure the directory for the config file exists
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(api_keys.dict(), f, indent=4)
        logging.info(f"API keys successfully saved to {CONFIG_FILE}.")
    except Exception as e:
        logging.error(f"Error writing API keys to {CONFIG_FILE}: {e}")
        raise e
