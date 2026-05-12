"""
Common response schemas used across multiple endpoints.
"""

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Standard error response returned to the client on any failure.

    This shape is consistent across all error paths so the frontend
    can always expect `{ "error": "..." }`.
    """

    error: str = Field(..., description="A human-readable error message.")
