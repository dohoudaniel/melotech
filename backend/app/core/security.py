"""
Security module — lightweight prompt-injection detection.

Contains a simple, rule-based filter that scans user input for common
instruction-hijacking patterns. This is intentionally explicit rather
than clever; readability and auditability are more important than
catching every theoretical edge case.
"""

import re
from typing import Optional

from app.core.logging import logger


# Compiled regex patterns that match common prompt-injection phrases.
# Each pattern is case-insensitive and allows minor word-boundary variations.
_INJECTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+above",
        r"disregard\s+(all\s+)?previous",
        r"act\s+as\s+(a\s+|an\s+)?",
        r"you\s+are\s+now\s+a",
        r"pretend\s+(to\s+be|you\s+are)",
        r"system\s*prompt",
        r"developer\s*message",
        r"reveal\s+(your\s+)?(instructions|prompt|system)",
        r"print\s+(all\s+)?(hidden\s+)?instructions",
        r"show\s+(me\s+)?(your\s+)?(hidden\s+)?prompt",
        r"what\s+are\s+your\s+instructions",
        r"override\s+(your\s+)?instructions",
        r"new\s+instructions",
        r"forget\s+(everything|all|your)",
        r"do\s+not\s+follow",
        r"bypass\s+(filters|safety|rules)",
        r"jailbreak",
        r"<\s*script",
        r"\{\{.*\}\}",  # Template injection markers.
    ]
]


def detect_prompt_injection(text: str) -> Optional[str]:
    """
    Scan the given text for common prompt-injection patterns.

    Args:
        text: The user-provided string to inspect.

    Returns:
        A short human-readable reason if a suspicious pattern is detected,
        or None if the input looks clean.
    """
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(text):
            logger.warning("Prompt injection attempt detected in input.")
            return "The input contains disallowed instructions or suspicious content."

    return None
