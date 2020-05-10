# -*- coding: utf-8 -*-

"""Defines class representing a valid url."""

import validators  # type: ignore

from logtweet.source.retrieve import AbstractValidSource


# TODO: (4) Implement ValidOnlineSource based on AbstractValidOnlineSource
class ValidSourceURL(AbstractValidSource):
    """Valid URL class."""

    # def __init__(self, url: str):
    #     """
    #     Initialize ValidUrl object.

    #     Initialization fails with exception if the passed URL is not valid.

    #     Arguments:
    #         url (str): URL string to be validated.

    #     Raises:
    #         NotAUrlError: if the passed url is not a valid URL.

    #     """
    #     if not is_valid_url(url):
    #         raise NotAUrlError(url)
    #     self.url = url


    def is_valid(url: str) -> bool:
        """
        Check if the given URL is valid.

        Arguments:
            url (str): URL that is to be validated.

        Returns:
            bool: Expresses if the given URL is valid.

        """
        is_url = validators.url(url)
        if is_url is not True:
            return False
        return True
