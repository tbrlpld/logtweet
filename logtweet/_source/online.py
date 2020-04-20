# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

from typing import Literal

import requests
import validators  # type: ignore

from logtweet._source.exceptions import NotAUrlError


class OnlineLogSource(object):
    """Valid online log source."""

    def __init__(self, source_string: str):
        """
        Initialize OnlineLogSource object.

        During initialization, it is validated that the given ``source_string``
        is in fact a valid URL representation.

        Arguments:
            source_string (str): String that identifies the online resource
                which should be validated.

        Raises:
            NotAUrlError: if the given ``source_string`` does not represent a
                valid URL.

        """
        self.raise_for_invalid_url(source_string)
        self.source_string = source_string
        # self.get_content_from_online_source(self.source_string)

    @staticmethod
    def raise_for_invalid_url(source_string: str) -> None:
        """
        Raise an exception if the given source string is not a valid URL.

        Arguments:
            source_string (str): URL that is to be validated.

        Returns:
            True: if the given ``source_string`` is in fact a valid URL.

        Raises:
            NotAUrlError: if the given ``source_string`` does not represent a
                valid URL.

        """
        is_url = validators.url(source_string)
        if is_url is not True:
            raise NotAUrlError(source_string)

    def get_content_from_online_source(self, source_string: str = None) -> str:
        """Get content from online source."""
        if source_string is None:
            source_string = self.source_string
        response = requests.get(source_string)
        return response.text
