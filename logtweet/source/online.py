# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

import requests

from logtweet.source.retrieve import AbstractSourceContentRetriever


# TODO: (1) Implement OnlineSourceRetriever based on AbstractSourceRetriever
# TODO: (2) Require AbstractValidOnlineSurce as input
# TODO: (3) Define AbstractValidOnlineSource based on AbstractValidSource
class OnlineSourceContentRetriever(AbstractSourceContentRetriever):
    """Valid online log source."""
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
