# -*- coding: utf-8 -*-

"""Defines class representing a valid online source for the log."""


import validators

from logtweet._source.exceptions import NotAURLError


class OnlineLogSource(object):
    """Valid online log source."""

    def __init__(self, source_string: str):
        """
        Initialize OnlineLogSource object.

        During initialization, it is validated that the given ``source_string``
        is in fact a valid URL representation.

        Raises:
            NotAURLError: if the given ``source_string`` does not represent a
                valid URL.

        """
        is_url = validators.url(source_string)
        if is_url is not True:
            raise NotAURLError
        self.source_string = source_string
