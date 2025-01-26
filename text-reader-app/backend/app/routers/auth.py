"""
Authentication and API Key management router.

This module handles authentication via token verification and manages API keys.
Provides endpoints for retrieving and validating API keys.
"""

from fastapi import APIRouter, Header, HTTPException, status, Depends
from typing import Dict, Any
from ..schemas import APIKeys
from ..crud import read_api_keys, write_api_keys
import os

router = APIRouter()

# Environment variable for authentication, fallback to default if not set
SECRET_TOKEN = os.getenv("APP_SECRET_TOKEN", "default_secret_token")


def verify_token(x_token: str = Header(...)) -> str:
    """
    Verify the authentication token from request headers.

    Args:
        x_token (str): Token from request header

    Returns:
        str: Valid token

    Raises:
        HTTPException: If token is invalid or missing
    """
    if x_token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return x_token


@router.get("/api_keys/", response_model=APIKeys, dependencies=[Depends(verify_token)])
def get_api_keys() -> APIKeys:
    """
    Retrieve stored API keys.

    Returns:
        APIKeys: Object containing API keys

    Raises:
        HTTPException: If API keys are not found
    """
    api_keys = read_api_keys()
    if not api_keys:
        raise HTTPException(status_code=404, detail="API keys not found")
    return api_keys


@router.get("/")
def read_root() -> Dict[str, Any]:
    """
    Root endpoint for the API Key service.

    Returns:
        dict: Welcome message
    """
    return {"message": "API Key Settings Service"}


@router.post("/api_keys/", response_model=APIKeys, dependencies=[Depends(verify_token)])
def save_api_keys(api_keys: APIKeys) -> APIKeys:
    """
    Save API keys.

    Args:
        api_keys (APIKeys): Object containing API keys to save

    Returns:
        APIKeys: Saved API keys

    Raises:
        HTTPException: If there's an error saving the keys
    """
    try:
        write_api_keys(api_keys)
        return api_keys
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving API keys: {str(e)}"
        )
