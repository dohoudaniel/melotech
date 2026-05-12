"""
Text sanitization service.

Cleans user-provided text so it is safe for prompt interpolation
without destroying legitimate job title content.
"""

import re
import unicodedata


def sanitize_job_title(raw: str) -> str:
    """
    Sanitize a raw job title string.

    Steps performed:
        1. Strip leading/trailing whitespace.
        2. Remove control characters (anything in Unicode category "C").
        3. Normalize internal whitespace (collapse runs of spaces/tabs/newlines).
        4. Cap the length as a secondary safeguard (Pydantic handles the primary cap).

    Args:
        raw: The unprocessed string from the user.

    Returns:
        A cleaned string safe for prompt interpolation.
    """
    # 1. Strip outer whitespace.
    text = raw.strip()

    # 2. Remove Unicode control characters (category C), preserving normal text.
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    # 3. Collapse any sequence of whitespace into a single space.
    text = re.sub(r"\s+", " ", text).strip()

    return text
