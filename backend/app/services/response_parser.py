"""
Response parser service.

Takes the raw text returned by any AI provider and converts it into
a validated list of QuestionItem objects. Handles common format issues
such as markdown code fences and trailing commas.
"""

import json
import re
from typing import Optional

from app.core.logging import logger
from app.schemas.questions import QuestionItem


def parse_ai_response(raw_text: str) -> Optional[list[QuestionItem]]:
    """
    Parse the raw AI response text into a list of QuestionItem objects.

    The function attempts to extract valid JSON from the response,
    handling common formatting quirks returned by LLMs (e.g. markdown
    code blocks wrapping the JSON).

    Args:
        raw_text: The raw string returned by the AI provider.

    Returns:
        A list of exactly 3 QuestionItem objects if parsing succeeds,
        or None if the response is malformed or does not meet requirements.
    """
    cleaned = _strip_markdown_fences(raw_text.strip())

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("AI response is not valid JSON.")
        return None

    # The response must be a dict with a "questions" key.
    if not isinstance(data, dict) or "questions" not in data:
        logger.warning("AI response JSON does not contain a 'questions' key.")
        return None

    questions_raw = data["questions"]

    # We need exactly 3 items.
    if not isinstance(questions_raw, list) or len(questions_raw) != 3:
        logger.warning(
            "AI response contains %s questions instead of 3.",
            len(questions_raw) if isinstance(questions_raw, list) else "non-list",
        )
        return None

    # Validate each item against the QuestionItem schema.
    try:
        items = [QuestionItem(**q) for q in questions_raw]
    except Exception:
        logger.warning("One or more question items failed validation.")
        return None

    return items


def _strip_markdown_fences(text: str) -> str:
    """
    Remove markdown code fences (```json ... ```) that LLMs sometimes
    wrap around their JSON output.

    Args:
        text: The raw text that may contain code fences.

    Returns:
        The text with outer code fences removed.
    """
    # Match ```json ... ``` or ``` ... ```.
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?\s*```$"
    match = re.match(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text
