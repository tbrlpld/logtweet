# -*- coding: utf-8 -*-

"""Custom exceptions for use in relation to source handling."""


class LogtweetSourceError(Exception):
    """Base exception class for use in this module."""

    pass  # noqa: WPS420, WPS604


class NotAUrlError(LogtweetSourceError):
    """Raised when a source string is expected to be a URL but is not."""

    def __init__(self, source_string: str = ""):
        """
        Initialize ``NotAUrlError``.

        Arguments:
            source_string (str): Provide the source string that is not a URL.
                Optional argument. Defaults to empty string. If not provided,
                the source string is not shown to the user.

        """
        self.source_string = source_string

        # Add parenthesis around source string only if not empty.
        source_string_in_msg = ""
        if self.source_string:
            source_string_in_msg = "'{0}'".format(source_string)

        self.message = "The given source string {0} is not a URL!".format(
            source_string_in_msg,
        )
        super().__init__(self.message)


class HTTPStatusError(LogtweetSourceError):
    """Raised when response status code indicates error, e.g. 404."""

    pass  # noqa: WPS420, WPS604


class RequestError(LogtweetSourceError):
    """Raised when issue request to source."""

    def __init__(self, url: str):
        """
        Initialize ``RequestError``.

        Arguments:
            url (str): URL that the request was sent to when the error
                occurred.

        """
        self.url = url

        self.message = "The request to '{0}' failed!".format(
            self.url,
        )
        super().__init__(self.message)
