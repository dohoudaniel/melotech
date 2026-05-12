"""
Gemini client service — primary AI provider.

Wraps the Google Generative AI SDK to send a prompt and return
the model's raw text response.
"""

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
        Exception: Any error from the SDK is allowed to propagate so
                   the orchestrator can catch it and trigger the fallback.
    """
    logger.info("Calling Gemini model: %s", model)

    # Initialize the Gemini client with the provided API key.
    client = genai.Client(api_key=api_key)

    # Build the request with a system instruction and the user content.
    response = client.models.generate_content(
        model=model,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        ),
    )

    # Extract the text from the first candidate.
    result_text = response.text
    logger.info("Gemini responded successfully.")
    return result_text
