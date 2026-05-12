"""
Groq client service — fallback AI provider.

Wraps the Groq SDK to send a prompt and return the model's raw text
response. Used only when the primary Gemini provider fails.

IMPORTANT: The Groq SDK's chat.completions.create() is synchronous.
We run it in a thread pool executor to avoid blocking the FastAPI
event loop and starving other concurrent requests.
"""

import asyncio
from functools import partial

from groq import Groq

from app.core.logging import logger


async def call_groq(
    api_key: str,
    model: str,
    system_prompt: str,
    user_message: str,
) -> str:
    """
    Send a prompt to the Groq model and return the raw text response.

    Args:
        api_key: The Groq API key (loaded from environment).
        model: The model identifier (e.g. "llama-3.3-70b-versatile").
        system_prompt: The system instruction for the model.
        user_message: The user-facing message containing the job title.

    Returns:
        The raw text content of the model's response.

    Raises:
        ValueError: If the model returns an empty or missing response.
        Exception: Any error from the SDK is allowed to propagate so
                   the orchestrator can catch it and return a final error.
    """
    logger.info("Calling Groq model (fallback): %s", model)

    # Initialize the Groq client with the provided API key.
    client = Groq(api_key=api_key)

    # Build the synchronous API call as a partial so it can be dispatched
    # to a thread pool executor without blocking the async event loop.
    sync_call = partial(
        client.chat.completions.create,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        # Temperature of 0.7 — same value used in the Gemini client for
        # consistency. See gemini_client.py for the rationale.
        temperature=0.7,
    )

    # Run the synchronous SDK call in a thread pool so the event loop
    # remains free to serve other requests concurrently.
    loop = asyncio.get_running_loop()
    chat_completion = await loop.run_in_executor(None, sync_call)

    # Defensive check: the choices list or message content can be empty
    # if the model fails to generate output or hits a safety filter.
    if not chat_completion.choices:
        raise ValueError("Groq returned no choices in the response.")

    result_text = chat_completion.choices[0].message.content
    if not result_text:
        raise ValueError("Groq returned an empty message content.")

    logger.info("Groq responded successfully.")
    return result_text
