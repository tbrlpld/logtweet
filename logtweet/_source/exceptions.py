# -*- coding: utf-8 -*-

"""Custom exceptions for use in relation to source handling."""


class LogtweetSourceError(Exception):
    """Base exception class for use in this module."""
    pass


class NotAURLError(LogtweetSourceError):
    """Raised when a source string is expected to be a URL but is not."""
    pass

