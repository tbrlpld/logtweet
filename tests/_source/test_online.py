# -*- coding: utf-8 -*-

"""Tests for the OnlineLogSource class."""

import pytest  # type: ignore

# Tests for reaching an online source require a working online connection.
# Or I need to mock the function that represents the availability of an online
# source.


def test_valid_url_creates_instance():
    from logtweet._source.online import OnlineLogSource

    instance = OnlineLogSource("https://example.com")

    assert isinstance(instance, OnlineLogSource)


def test_invalid_url_raises_exception():
    from logtweet._source.online import OnlineLogSource
    from logtweet._source.exceptions import NotAUrlError

    with pytest.raises(NotAUrlError):
        OnlineLogSource("not a url, just a string")


def test_invalid_url_shown_in_raised_exception():
    from logtweet._source.online import OnlineLogSource
    from logtweet._source.exceptions import NotAUrlError
    source_string = "not a url, just a string"

    with pytest.raises(
        NotAUrlError,
        match=r"^The given source string '{0}' is not a URL!".format(
            source_string,
        ),
    ):
        OnlineLogSource(source_string)
