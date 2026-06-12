"""Reusable logging configuration for project modules.

Production applications should configure logging in one place instead of each
module calling ``basicConfig`` independently. Modules can import
``get_logger(__name__)`` for a named logger, while application entry points can
call ``configure_logging()`` once during startup.
"""

from __future__ import annotations

import logging
import os
from typing import Final


LOG_LEVEL_ENV_VAR: Final[str] = "LOG_LEVEL"
DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging(level: int | str | None = None, *, force: bool = False) -> None:
    """Configure root logging for command-line scripts or services.

    Args:
        level: Logging level as an integer, a level name, a numeric string, or
            ``None``. When ``None``, ``LOG_LEVEL`` is read from the environment
            and defaults to ``INFO``.
        force: Passed to ``logging.basicConfig``. Use ``True`` in tests or
            scripts that intentionally replace existing handlers.

    Raises:
        TypeError: If ``level`` has an unsupported type.
        ValueError: If ``level`` is an unknown logging level name.
    """
    logging.basicConfig(
        level=_coerce_log_level(level),
        format=DEFAULT_LOG_FORMAT,
        force=force,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger with a ``NullHandler`` attached once.

    Adding a ``NullHandler`` prevents library modules from emitting warnings in
    applications that have not configured logging yet, while still allowing
    messages to propagate when the application does configure logging.
    """
    logger = logging.getLogger(name)

    if not any(isinstance(handler, logging.NullHandler) for handler in logger.handlers):
        logger.addHandler(logging.NullHandler())

    return logger


def _coerce_log_level(level: int | str | None) -> int:
    """Normalize supported logging level inputs to an integer."""
    if level is None:
        level = os.getenv(LOG_LEVEL_ENV_VAR, "DEBUG")

    if isinstance(level, bool):
        raise TypeError("level must be an integer, string, or None")

    if isinstance(level, int):
        return level

    if isinstance(level, str):
        normalized_level = level.strip().upper()

        if normalized_level.isdigit():
            return int(normalized_level)

        resolved_level = logging.getLevelName(normalized_level)
        if isinstance(resolved_level, int):
            return resolved_level

        raise ValueError(f"Unknown logging level: {level}")

    raise TypeError("level must be an integer, string, or None")
