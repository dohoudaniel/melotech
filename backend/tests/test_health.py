"""
Tests for the health check endpoint.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
def client():
    """Provide an async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health_returns_ok(client):
    """GET /health should return status ok."""
    async with client as c:
        response = await c.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_root_returns_status(client):
    """GET / should return application info."""
    async with client as c:
        response = await c.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "app" in data
