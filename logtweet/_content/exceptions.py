# -*- coding: utf-8 -*-

"""Custom exceptions for use in relation to content handling."""


class LogtweetContentError(Exception):
    """Base exception class for use in this module."""

    pass  # noqa: WPS420, WPS604


class NoProgressPargraphs(LogtweetContentError):
    """Raised when response status code indicates error, e.g. 404."""

    def __init__(self):
        """
        Initialize ``NoProgressPargraphs``.

        Arguments:
            source_string (str): Provide the source string that is not a URL.
                Optional argument. Defaults to empty string. If not provided,
                the source string is not shown to the user.

        """
        self.message = "Could no retrieve any progress paragraphs!"
        super().__init__(self.message)
