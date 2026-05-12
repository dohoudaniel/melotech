"""
Questions route.

Handles the POST /questions endpoint — the core product feature.
Validates the incoming job title, sanitizes it, checks for injection
attempts, then delegates to the AI orchestrator.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.config import Settings, get_settings
from app.core.logging import logger
from app.core.security import detect_prompt_injection
from app.schemas.questions import QuestionRequest, QuestionsResponse
from app.schemas.common import ErrorResponse
from app.services.sanitization import sanitize_job_title
from app.services.ai_orchestrator import generate_questions, AIProviderError

router = APIRouter()


# -----------------------------------------------------------------
# POST /questions
#
# This is the core endpoint of the MeloTech product. The full pipeline:
#   1. Pydantic validates the request body (job_title length, type).
#   2. The route sanitizes the job title (strip, collapse whitespace).
#   3. The route checks for prompt-injection patterns.
#   4. The AI orchestrator calls Gemini (primary) or Groq (fallback).
#   5. The response is parsed, validated, and returned as structured JSON.
#
# Error codes:
#   400 — invalid input or injection attempt
#   503 — both AI providers are unavailable
#   500 — unexpected server error (catch-all, never leaks internals)
# -----------------------------------------------------------------


@router.post(
    "/questions",
    response_model=QuestionsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid or suspicious input."},
        503: {"model": ErrorResponse, "description": "AI providers unavailable."},
    },
)
async def create_questions(
    body: QuestionRequest,
    settings: Settings = Depends(get_settings),
) -> QuestionsResponse | JSONResponse:
    """
    Generate 3 interview questions for the given job title.

    Pipeline:
        1. Sanitize the job title.
        2. Check for prompt-injection patterns.
        3. Call the AI orchestrator (Gemini → Groq fallback).
        4. Return structured JSON with exactly 3 questions.

    Args:
        body: The validated request body containing the job title.
        settings: Application settings injected by FastAPI.

    Returns:
        A QuestionsResponse on success, or a JSONResponse with an
        error payload on failure.
    """
    logger.info("Received question generation request.")

    # --- Step 1: Sanitize ---
    clean_title = sanitize_job_title(body.job_title)

    # After sanitization the title might be empty.
    if not clean_title:
        logger.warning("Job title was empty after sanitization.")
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error="Please provide a valid job title.").model_dump(),
        )

    # --- Step 2: Injection check ---
    injection_reason = detect_prompt_injection(clean_title)
    if injection_reason:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error=injection_reason).model_dump(),
        )

    # --- Step 3: Generate questions ---
    try:
        questions = await generate_questions(clean_title, settings)
    except AIProviderError as exc:
        logger.error("AI orchestrator failed: %s", str(exc))
        return JSONResponse(
            status_code=503,
            content=ErrorResponse(error=str(exc)).model_dump(),
        )
    except Exception:
        # Catch-all for truly unexpected errors. Never expose internals.
        logger.exception("Unexpected error during question generation.")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="An unexpected error occurred. Please try again later."
            ).model_dump(),
        )

    # --- Step 4: Return structured response ---
    return QuestionsResponse(questions=questions)
