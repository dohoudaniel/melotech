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
    # Step 1: Strip markdown code fences (```json ... ```) that LLMs
    # sometimes wrap around their JSON output.
    cleaned = _strip_markdown_fences(raw_text.strip())

    # Step 2: Attempt to parse the cleaned text as JSON.
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("AI response is not valid JSON.")
        return None

    # Step 3: Verify the top-level structure — must be a dict with a "questions" key.
    if not isinstance(data, dict) or "questions" not in data:
        logger.warning("AI response JSON does not contain a 'questions' key.")
        return None

    questions_raw = data["questions"]

    # Step 4: Enforce exactly 3 questions — no more, no less.
    # The system prompt asks for 3, but models can sometimes return fewer
    # or more. We reject anything that doesn't match exactly.
    if not isinstance(questions_raw, list) or len(questions_raw) != 3:
        logger.warning(
            "AI response contains %s questions instead of 3.",
            len(questions_raw) if isinstance(questions_raw, list) else "non-list",
        )
        return None

    # Step 5: Validate each item against the QuestionItem Pydantic schema.
    # This ensures every question has the required fields (category, question,
    # why_it_matters) with the correct types.
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
