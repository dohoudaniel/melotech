"""
AI orchestrator service.

Coordinates the full question-generation flow:
    1. Build the prompt.
    2. Call Gemini (primary).
    3. Parse the response.
    4. If Gemini fails or returns malformed output, fall back to Groq.
    5. If Groq also fails, raise a clear error.

This is the only service the route handler needs to call.
"""

from typing import Optional

from app.core.config import Settings
from app.core.logging import logger
from app.schemas.questions import QuestionItem
from app.services.prompt_builder import build_system_prompt, build_user_message
from app.services.gemini_client import call_gemini
from app.services.groq_client import call_groq
from app.services.response_parser import parse_ai_response


class AIProviderError(Exception):
    """Raised when both AI providers fail to return usable results."""
    pass


async def generate_questions(
    job_title: str,
    settings: Settings,
) -> list[QuestionItem]:
    """
    Generate 3 interview questions for the given job title.

    Tries the Gemini provider first. If that fails for any reason
    (network, rate limit, malformed output), it tries Groq once.
    If both fail, an AIProviderError is raised.

    Args:
        job_title: The sanitized, validated job title.
        settings: Application settings containing API keys and model names.

    Returns:
        A list of exactly 3 QuestionItem objects.

    Raises:
        AIProviderError: If neither provider returns a valid result.
    """
    system_prompt = build_system_prompt()
    user_message = build_user_message(job_title)

    # --- Attempt 1: Gemini (primary) ---
    questions = await _try_provider(
        provider_name="Gemini",
        call_fn=lambda: call_gemini(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            system_prompt=system_prompt,
            user_message=user_message,
        ),
    )
    if questions:
        return questions

    # --- Attempt 2: Groq (fallback) ---
    logger.info("Falling back to Groq provider.")
    questions = await _try_provider(
        provider_name="Groq",
        call_fn=lambda: call_groq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            system_prompt=system_prompt,
            user_message=user_message,
        ),
    )
    if questions:
        return questions

    # Both providers failed.
    logger.error("Both Gemini and Groq failed to produce valid questions.")
    raise AIProviderError(
        "Unable to generate interview questions at this time. Please try again later."
    )


async def _try_provider(
    provider_name: str,
    call_fn,
) -> Optional[list[QuestionItem]]:
    """
    Attempt to call a single AI provider and parse its response.

    Args:
        provider_name: A human-readable label used for logging (e.g. "Gemini").
        call_fn: An async callable that returns the raw text from the provider.

    Returns:
        A list of QuestionItem objects if the call and parsing succeed,
        or None if any step fails.
    """
    try:
        raw_text = await call_fn()
    except Exception as exc:
        # Log the failure reason without exposing secrets.
        logger.warning(
            "%s provider call failed: %s",
            provider_name,
            str(exc),
        )
        return None

    # Attempt to parse the raw text into structured question items.
    questions = parse_ai_response(raw_text)
    if questions is None:
        logger.warning("%s returned a response that could not be parsed.", provider_name)
        return None

    return questions
