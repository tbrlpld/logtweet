# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

from typing import Literal

import requests
import validators  # type: ignore

from logtweet._source.exceptions import (  # noqa: WPS436
    NotAUrlError,
    HTTPStatusError,
    RequestError,
)


class OnlineLogSource(object):
    """Valid online log source."""

    def __init__(self, source_string: str):
        """
        Initialize OnlineLogSource object.

        During initialization, it is validated that the given ``source_string``
        is in fact a valid URL representation.

        Also, the online source is only valid if the content can successfully
        be retrieved. Thus, a successful instantiation makes the log content
        available. If anything fails while retrieving the content, the
        instantiation fails and no element is created.

        Arguments:
            source_string (str): String that identifies the online resource
                which should be validated.

        Raises:
            NotAUrlError: if the given ``source_string`` does not represent a
                valid URL.

        """
        # TODO: Extract the valid URL into a separate type and only accept that
        #       type for further processing.
        self.raise_for_invalid_url(source_string)
        self.url = source_string
        self._content = self.get_content_from_url(self.url)

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

    @staticmethod
    def get_content_from_url(url: str) -> str:
        """
        Get content from online source.

        This function requires the passed string to be a valid URL. This
        expectation should be enforced. So another type that only works for
        valid URLs might make sense.
        """

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            raise RequestError(url)

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise HTTPStatusError(error)
        return response.text

    @property
    def content(self):
        return self._content
