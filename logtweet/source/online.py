# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""

import requests

from logtweet._source.exceptions import (  # noqa: WPS436
    HTTPStatusError,
    RequestError,
)



# TODO: (1) Implement OnlineSourceRetriever based on AbstractSourceRetriever
# TODO: (2) Require AbstractValidOnlineSurce as input
# TODO: (3) Define AbstractValidOnlineSource based on AbstractValidSource
class OnlineLogSource(object):
    """Valid online log source."""

    def __init__(self, url: str):
        """
        Initialize OnlineLogSource object.

        During initialization, it is validated that the given `url`
        is in fact a valid URL representation.

        Also, the online source is only valid if the content can successfully
        be retrieved. Thus, a successful instantiation makes the  `content`
        available in the same named property. If anything fails while
        retrieving the content, the instantiation fails and no element is
        created. The occurring exceptions are not caught and populate to the
        caller.

        Parameters
        ----------
        url : str
            String that identifies the online resource which should
            be validated.

        Raises
        ------
        NotAUrlError
            If the passed URL is not a valid URL.
        RequestError
            When the network connection to the URL target fails.
        HTTPStatusError
            When the URL host responds with an error status code.

        # noqa: DAR402

        """
        self.url = ValidUrl(url)
        # TODO: Accept the concrete URL validator as a parameter.
        # TODO: Define an abstract URL validator that defines what the
        #       validator needs to provide from this class' perspective.

        self._content = get_content_from_url(self.url)  # noqa: WPS110

    @property  # noqa: WPS110
    def content(self):
        """
        Return online log content.

        Returns
        -------
        str
            Content of online log source.

        """
        return self._content  # noqa: WPS110

def get_content_from_url(valid_url: ValidUrl) -> str:
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
