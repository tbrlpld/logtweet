# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

import requests

from logtweet._source.exceptions import (  # noqa: WPS436
    HTTPStatusError,
    RequestError,
)
from logtweet._source.valid_url import ValidUrl


class OnlineLogSource(object):
    """Valid online log source."""

    def __init__(self, source_string: str):
        """
        Initialize OnlineLogSource object.

        During initialization, it is validated that the given ``source_string``
        is in fact a valid URL representation.

        Also, the online source is only valid if the content can successfully
        be retrieved. Thus, a successful instantiation makes the  ``content``
        available in the same named property. If anything fails while
        retrieving the content, the instantiation fails and no element is
        created. The occurring exceptions are not caught and populate to the
        caller.

        Arguments:
            source_string (str): String that identifies the online resource
                which should be validated.

        Raises:
            NotAUrlError: when the passed source string is not a valid URL.
            RequestError: when the network connection to the URL target
                fails.
            HTTPStatusError: when the URL host responds with an error status
                code.
        """

        self.url = ValidUrl(source_string)  # Raises NotAUrlError

        self._content = self.get_content_from_url(self.url)

    @staticmethod
    def get_content_from_url(valid_url: ValidUrl) -> str:
        """
        Get content from online source.

        Arguments:
            valid_url (ValidUrl): Validated url object from which the content
                should be retrieved.

        Raises:
            RequestError: when the network connection to the URL target
                fails.
            HTTPStatusError: when the URL host responds with an error status
                code.

        """
        if not isinstance(valid_url, ValidUrl):
            raise TypeError(
                "Expected `ValidUrl` got {0}".format(type(valid_url)),
            )

        try:
            response = requests.get(valid_url.url)
        except requests.exceptions.RequestException:
            raise RequestError(valid_url.url)

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise HTTPStatusError(error)
        return response.text

    @property
    def content(self):
        return self._content
