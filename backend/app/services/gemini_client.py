"""
Gemini client service — primary AI provider.

Wraps the Google Generative AI SDK to send a prompt and return
the model's raw text response.

IMPORTANT: The google-genai SDK's generate_content() is synchronous.
We run it in a thread pool executor to avoid blocking the FastAPI
event loop and starving other concurrent requests.
"""

import asyncio
from functools import partial

from google import genai
from google.genai import types

from app.core.logging import logger


async def call_gemini(
    api_key: str,
    model: str,
    system_prompt: str,
    user_message: str,
) -> str:
    """
    Send a prompt to the Gemini model and return the raw text response.

    Args:
        api_key: The Gemini API key (loaded from environment).
        model: The model identifier (e.g. "gemini-3.1-pro-preview").
        system_prompt: The system instruction for the model.
        user_message: The user-facing message containing the job title.

    Returns:
        The raw text content of the model's response.

    Raises:
        ValueError: If the model returns an empty or missing response.
        Exception: Any error from the SDK is allowed to propagate so
                   the orchestrator can catch it and trigger the fallback.
    """
    logger.info("Calling Gemini model: %s", model)

    # Initialize the Gemini client with the provided API key.
    client = genai.Client(api_key=api_key)

    # Build the synchronous API call as a partial so it can be dispatched
    # to a thread pool executor without blocking the async event loop.
    sync_call = partial(
        client.models.generate_content,
        model=model,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            # Temperature of 0.7 balances variety (different questions across
            # repeated requests) with reliability (structured JSON output).
            # Lower values (0.3) give repetitive results; higher values (0.9+)
            # risk malformed output.
            temperature=0.7,
        ),
    )

    # Run the synchronous SDK call in a thread pool so the event loop
    # remains free to serve other requests concurrently.
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, sync_call)

    # Defensive check: response.text can be None if the model returns
    # no candidates (e.g. safety filter triggered, empty generation).
    result_text = response.text
    if not result_text:
        raise ValueError("Gemini returned an empty response.")

    logger.info("Gemini responded successfully.")
    return result_text
