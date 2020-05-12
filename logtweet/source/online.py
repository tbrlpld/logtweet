# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

import requests

from logtweet.source.retrieve import (
    AbstractValidSource,
    AbstractSourceContentRetriever,
)


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
        """Override for type annotation only."""
        self.valid_source: AbstractValidOnlineSource
        super().__init__(valid_source)

    # TODO: (1) Implement concrete method to retrieve online source content
    def get_content():
        pass


def get_content_from_url(valid_url: str) -> str:
    """
    Get content from online source.

    Parameters
    ----------
    valid_url : ValidUrl
         Validated url object from which the content should be retrieved.

    Returns
    -------
    str
        Content retrieved from the URL.

    Raises
    ------
    TypeError
        When the passed URL is not of type `ValidUrl`.
    RequestError
        When the network connection to the URL target fails.
    HTTPStatusError
        When the URL host responds with an error status code.

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
