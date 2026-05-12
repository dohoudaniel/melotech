"""
Text sanitization service.

Cleans user-provided text so it is safe for prompt interpolation
without destroying legitimate job title content.
"""

import re
import unicodedata

# Maximum number of characters allowed after sanitization.
# This is a secondary safeguard — Pydantic validates max_length on the
# raw input first, but sanitization could theoretically alter the length.
_MAX_SANITIZED_LENGTH = 100


def sanitize_job_title(raw: str) -> str:
    """
    Sanitize a raw job title string.

    Steps performed:
        1. Strip leading/trailing whitespace.
        2. Remove control characters (anything in Unicode category "C").
        3. Normalize internal whitespace (collapse runs of spaces/tabs/newlines).
        4. Cap the length as a secondary safeguard.

    Args:
        raw: The unprocessed string from the user.

    Returns:
        A cleaned string safe for prompt interpolation.
    """
    # 1. Strip outer whitespace.
    text = raw.strip()

    # 2. Remove Unicode control characters (category C), preserving normal text.
    # This catches null bytes, backspaces, and other invisible characters that
    # could be used to confuse the AI model or bypass pattern matching.
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    # 3. Collapse any sequence of whitespace into a single space.
    text = re.sub(r"\s+", " ", text).strip()

    # 4. Enforce a hard length cap after all transformations.
    # This ensures the sanitized output never exceeds the expected limit,
    # even if the raw input somehow passed Pydantic's max_length check.
    text = text[:_MAX_SANITIZED_LENGTH]

    return text
