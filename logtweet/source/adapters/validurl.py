# -*- coding: utf-8 -*-

"""Defines class representing a valid url."""

import validators  # type: ignore

from logtweet.source.usecases import retrieve as ucretrieve
from logtweet.source.adapters import onlineretriever as adaptonline


class NotAUrlError(ucretrieve.SourceValidationError):
    """Raised when a source string is expected to be a URL but is not."""

    def __init__(self, source_string: str = ""):
        """
        Initialize `NotAUrlError`.

        Parameters
        ----------
        source_string : str)
                Provide the source string that is not a URL.
                Optional argument. Defaults to empty string. If not provided,
                the source string is not shown to the user.

        """
        self.source_string = source_string

        # Add parenthesis around source string only if not empty.
        source_string_in_msg = ""
        if self.source_string:
            source_string_in_msg = "'{0}'".format(source_string)

        self.message = "The given source string {0} is not a URL!".format(
            source_string_in_msg,
        )
        super().__init__(self.message)


class ValidSourceURL(adaptonline.AbstractValidOnlineSource):
    """Valid URL class."""

    def __init__(self, url: str) -> None:
        """
        Initialize `ValidSourceURL`.

        Parameters
        ----------
        url : str
            URL to validate.

        Raises
        ------
        NotAUrlError
            Raised if the passed URL can not be validated as a URL.

        """
        try:
            super().__init__(url)
        except ucretrieve.SourceValidationError:
            raise NotAUrlError(url)

    @staticmethod
    def is_valid(url: str) -> bool:  # noqa: WPS602
        """
        Check if the given URL is valid.

        Parameters
        ----------
        url :str
            URL that is to be validated.

        Returns
        -------
        bool
             Expresses if the given URL is valid.

        """
        is_url = validators.url(url)
        if is_url is not True:
            return False
        return True
