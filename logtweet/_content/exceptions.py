# -*- coding: utf-8 -*-

"""Custom exceptions for use in relation to content handling."""


class LogtweetContentError(Exception):
    """Base exception class for use in this module."""

    pass  # noqa: WPS420, WPS604


class NoProgressPargraphsError(LogtweetContentError):
    """Raise when no progress paragraphs exist."""

    def __init__(self):
        """Initialize ``NoProgressPargraphs``."""
        self.message = "No progress paragraphs found!"
        super().__init__(self.message)


class EmptyProgressParagraphsError(LogtweetContentError):
    """Raise when progress paragraphs are empty exist."""

    def __init__(self):
        """Initialize ``NoProgressPargraphs``."""
        self.message = "No content in progress paragraphs found!"
        super().__init__(self.message)


class StringJoiningError(LogtweetContentError):
    """Raise when issue with joining strings."""

    pass  # noqa: WPS420, WPS604
