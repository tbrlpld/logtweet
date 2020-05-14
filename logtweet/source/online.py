# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

from typing import Optional

import requests

from logtweet.source.usecases.retrieve import (
    AbstractValidSource,
    AbstractSourceContentRetriever,
    SourceContentRetrievalError,
)


class RequestError(SourceContentRetrievalError):
    """Raised when issue request to source."""

    def __init__(self, url: str, err: Optional[Exception] = None):
        """
        Initialize ``RequestError``.

        Parameters
        ----------
        url : str
            URL that the request was sent to when the error occurred.
        err : Exception
            Original exception raised

        """
        self.url = url

        self.message = "The request to '{0}' failed!".format(self.url)
        if err:
            self.message += " The following error occurred:\n{0}".format(err)
        super().__init__(self.message)


class HTTPStatusError(SourceContentRetrievalError):
    """Raised when response status code indicates error, e.g. 404."""

    def __init__(self, url: str, status_code: int):
        """
        Initialize ``HTTPStatusError``.

        Parameters
        ----------
        url : str
            URL that from which the response with the bad status was returned.
        status_code : int
            Status code of the response

        """
        self.url = url
        self.status_code = status_code

        self.message = "Response from '{0}' failed with status: {1}!".format(
            self.url,
            self.status_code,
        )
        super().__init__(self.message)


class AbstractValidOnlineSource(AbstractValidSource):
    """
    Abstract class representing a valid online source.

    The validation method `is_valid` still needs to be implemented.

    This abstraction adds the `url` property.

    """

    @property
    def url(self) -> str:
        """
        URL of the validated online source.

        Returns
        -------
        str
            URL of the validated online source.

        """
        return self.source_string


class OnlineSourceContentRetriever(AbstractSourceContentRetriever):
    """Valid online log source."""

    valid_source_type = AbstractValidOnlineSource

    def __init__(self, valid_source: AbstractValidOnlineSource) -> None:
        """
        Override for type annotation only.

        Parameters
        ----------
        valid_source : AbstractValidOnlineSource
            Valid online source object. The object needs to be an instance
            of a subclass of `AbstractValidOnlineSource`.

        """
        self.valid_source: AbstractValidOnlineSource
        super().__init__(valid_source)

    def get_content(self) -> str:
        """
        Get content from online source.

        Returns
        -------
        str
            Content string retrieved from the online source.

        Raises
        ------
        RequestError
            When the network connection to the URL target fails.
        HTTPStatusError
            When the source host responds with an error status code (e.g. 404).

        """
        try:
            response = requests.get(self.valid_source.url)
        except requests.exceptions.RequestException as err:
            raise RequestError(self.valid_source.url, err)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise HTTPStatusError(self.valid_source.url, response.status_code)

        return response.text
