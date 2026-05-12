"""
MeloTech Backend — Application entry point.

Creates and configures the FastAPI application instance, including
CORS middleware and route registration. This is the file Uvicorn
points to when starting the server.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import logger
from app.routes import health, questions


def create_app() -> FastAPI:
    """
    Factory function that builds and returns the configured FastAPI app.

    Using a factory keeps configuration explicit and makes testing
    easier (you can create a fresh app per test run if needed).
    """
    settings = get_settings()

    # --- Startup validation ---
    # Check that all required environment variables are properly set.
    # This catches misconfiguration immediately rather than failing on the
    # first user request with a cryptic provider error.
    config_warnings = settings.validate_required_keys()
    for warning in config_warnings:
        logger.warning("CONFIG: %s", warning)

    # If both AI provider keys are missing, the app is non-functional.
    # Fail fast with a clear error rather than starting a broken server.
    if len(config_warnings) >= 2 and any("GEMINI" in w for w in config_warnings) and any("GROQ" in w for w in config_warnings):
        raise RuntimeError(
            "Both GEMINI_API_KEY and GROQ_API_KEY are missing or invalid. "
            "The server cannot generate questions without at least one AI provider. "
            "Please check your .env file."
        )

    app = FastAPI(
        title=settings.app_name,
        description=(
            "A minimal AI-powered backend that generates thoughtful "
            "interview questions from a job title."
        ),
        version="1.0.0",
        # Disable the docs in production if desired; kept on for now
        # so reviewers can explore the API easily.
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # --- CORS ---
    # The allowed origins are read from the environment so nothing is hardcoded.
    origins = [origin.strip() for origin in settings.cors_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Routes ---
    app.include_router(health.router)
    app.include_router(questions.router)

    # --- Root endpoint ---
    @app.get("/")
    async def root() -> dict:
        """Simple root endpoint with a brief status message."""
        return {
            "app": settings.app_name,
            "status": "running",
            "docs": "/docs",
        }

    # --- Global exception handler ---
    # Catches any unhandled exception and returns a safe JSON error
    # instead of leaking a stack trace to the client.
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"error": "An internal server error occurred."},
        )

    logger.info("%s backend started.", settings.app_name)
    return app


# The application instance Uvicorn will serve.
app = create_app()
