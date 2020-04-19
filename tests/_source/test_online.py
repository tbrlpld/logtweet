# -*- coding: utf-8 -*-

"""Tests for the OnlineLogSource class."""

import pytest  # type: ignore

# Tests for reaching an online source require a working online connection.
# Or I need to mock the function that represents the availability of an online
# source.


class TestInitialization(object):
    """Test the initialization of ``OnlineLogSource``."""
    def test_valid_url_creates_instance(self):
        from logtweet._source.online import OnlineLogSource

        instance = OnlineLogSource("https://example.com")

        assert isinstance(instance, OnlineLogSource)

    def test_invalid_url_raises_exception(self):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            OnlineLogSource("not a url, just a string")



class TestRaiseForInvalidUrlStaticMethod(object):
    """Test the static ``raise_for_invalid_url`` method."""
    def test_valid_url_returns_none(self):
        from logtweet._source.online import OnlineLogSource

        is_valid = OnlineLogSource.raise_for_invalid_url("https://example.com")

        assert is_valid is None

    def test_invalid_url_raises_exception(self):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            OnlineLogSource.raise_for_invalid_url("not a url, just a string")

    def test_invalid_url_shown_in_raised_exception(self):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError
        source_string = "not a url, just a string"

        with pytest.raises(
            NotAUrlError,
            match=r"^The given source string '{0}' is not a URL!".format(
                source_string,
            ),
        ):
            OnlineLogSource.raise_for_invalid_url(source_string)
