"""
Core configuration module.

Loads all environment variables from .env and exposes them as a typed,
validated Settings object. Nothing is hardcoded; every secret and
configurable value is read from the environment.
"""

import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


# Locate the .env file relative to the backend root directory.
# The backend root is two levels up from this file (backend/app/core/config.py).
_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded exclusively from environment variables.

    Every field maps to an environment variable of the same name (case-insensitive).
    Defaults are provided only for non-secret, structural values.
    """

    # --- Application ---
    app_name: str = Field(default="MeloTech", description="Display name of the application.")
    debug: bool = Field(default=False, description="Enable debug mode (never True in production).")

    # --- CORS ---
    cors_origins: str = Field(
        default="http://localhost:5173",
        description="Comma-separated list of allowed CORS origins.",
    )

    # --- AI Providers ---
    gemini_api_key: str = Field(
        default="",
        description="API key for Google Gemini. Required for the primary AI provider.",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash-preview-05-20",
        description="Model identifier for the Gemini provider.",
    )

    groq_api_key: str = Field(
        default="",
        description="API key for Groq. Required for the fallback AI provider.",
    )
    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Model identifier for the Groq provider.",
    )

    # --- Validation ---
    max_job_title_length: int = Field(
        default=100,
        description="Maximum number of characters allowed in a job title.",
    )

    model_config = ConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    """
    Return a Settings instance.

    Called once at app startup and injected where needed via FastAPI's
    dependency system. This avoids re-reading environment variables on
    every request.
    """
    return Settings()
