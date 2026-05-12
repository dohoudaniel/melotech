"""
Logging configuration module.

Sets up a single, consistent logger for the entire application.
Logs are kept clean: no secrets, no raw credentials, no personal data.
"""

import logging
import sys


def setup_logger(name: str = "melotech") -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name: The name of the logger. Defaults to 'melotech'.

    Returns:
        A logging.Logger instance with a stream handler writing to stdout.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if this function is called more than once.
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


# Shared logger instance used throughout the application.
logger = setup_logger()
