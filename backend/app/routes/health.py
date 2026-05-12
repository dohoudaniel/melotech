"""
Health check route.

Provides a simple endpoint for deployment probes and debugging.
"""

from fastapi import APIRouter

from app.core.logging import logger

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """
    Return a simple status object confirming the backend is running.

    Used by deployment health checks, uptime monitors, and quick
    manual verification.
    """
    logger.info("Health check accessed.")
    return {"status": "ok"}
