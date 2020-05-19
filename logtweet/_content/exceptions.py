# -*- coding: utf-8 -*-

"""Custom exceptions for use in relation to content handling."""

import typing


class LogtweetContentError(Exception):
    """Base exception class for use in this module."""

    pass  # noqa: WPS420, WPS604


class NoProgressPargraphsError(LogtweetContentError):
    """Raise when no progress paragraphs exist."""

    def __init__(self) -> None:
        """Initialize `NoProgressPargraphs`."""
        self.message = "No progress paragraphs found!"
        super().__init__(self.message)


class EmptyProgressParagraphsError(LogtweetContentError):
    """Raise when progress paragraphs are empty exist."""

    def __init__(self) -> None:
        """Initialize `EmptyProgressPargraphs`."""
        self.message = "No content in progress paragraphs found!"
        super().__init__(self.message)


class FirstStringLongerThanMaxError(LogtweetContentError):
    """Raise when issue with joining strings."""

    def __init__(
        self,
        strings: typing.Union[typing.List[str], typing.Tuple[str, ...]],
        max_len: int,
    ) -> None:
        """Initialize `FirstStringLongerThanMaxError`."""
        self.message = (
            "First string in sequence longer than maximum length."
            + " Can not join any strings."
            + " Maximum length: {0}".format(max_len)
            + ", Strings: {0}".format(max_len)
        )
        super().__init__(self.message)

