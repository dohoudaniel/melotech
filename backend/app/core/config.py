"""
Core configuration module.

Loads all environment variables from .env and exposes them as a typed,
validated Settings object. Nothing is hardcoded; every secret and
configurable value is read from the environment.
"""

from functools import lru_cache
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

    # Placeholder values that ship in .env.example and the test .env.
    # If a key is still set to one of these at startup, it means the
    # developer forgot to replace it with their real credentials.
    _PLACEHOLDER_VALUES = {
        "your_gemini_api_key_here",
        "your_groq_api_key_here",
        "test_key",
    }

    def validate_required_keys(self) -> list[str]:
        """
        Check that all required environment variables are set and not
        still using placeholder values from .env.example.

        Returns:
            A list of human-readable warning strings. An empty list
            means everything is configured correctly.
        """
        warnings: list[str] = []

        # Check Gemini API key.
        if not self.gemini_api_key or self.gemini_api_key.strip() in self._PLACEHOLDER_VALUES:
            warnings.append(
                "GEMINI_API_KEY is missing or still set to a placeholder. "
                "The primary AI provider will not work."
            )

        # Check Groq API key.
        if not self.groq_api_key or self.groq_api_key.strip() in self._PLACEHOLDER_VALUES:
            warnings.append(
                "GROQ_API_KEY is missing or still set to a placeholder. "
                "The fallback AI provider will not work."
            )

        # Check CORS origins.
        if not self.cors_origins or not self.cors_origins.strip():
            warnings.append(
                "CORS_ORIGINS is empty. The frontend will not be able to "
                "communicate with the backend."
            )

        return warnings


@lru_cache()
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Uses lru_cache so the .env file is read exactly once at startup.
    All subsequent calls (including FastAPI's Depends injection on
    every request) return the same cached object.
    """
    return Settings()
