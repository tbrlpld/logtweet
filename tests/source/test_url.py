# -*- coding: utf-8 -*-

"""Tests for the OnlineLogSource class."""

import pytest  # type: ignore


@pytest.fixture  # type: ignore
def valid_url_string() -> str:
    """Return string of a valid URL."""
    return "https://example.com"


@pytest.fixture  # type: ignore
def invalid_url_string() -> str:
    """Return string of an invalid URL."""
    return "not a url, just a string"


class TestIsValidStaticMethod(object):
    """Test the ``is_valid`` method."""

    def test_valid_url_string(
        self,
        valid_url_string: str,
    ) -> None:
        from logtweet.source.url import ValidSourceURL

        is_valid = ValidSourceURL.is_valid(valid_url_string)

        assert is_valid is True

    def test_invalid_url_string(
        self,
        invalid_url_string: str,
    ) -> None:
        from logtweet.source.url import ValidSourceURL

        is_valid = ValidSourceURL.is_valid(invalid_url_string)

        assert is_valid is False


class TestValidUrlInitialization(object):
    """Test initialization of ValidURL."""

    def test_valid_url_string_creates_object(self, valid_url_string):
        from logtweet._source.valid_url_string import ValidUrl

        url_obj = ValidUrl(valid_url_string)

        assert isinstance(url_obj, ValidUrl)

    def test_valid_object_has_url_property(self, valid_url_string):
        from logtweet._source.valid_url_string import ValidUrl

        url_obj = ValidUrl(valid_url_string)

        assert url_obj.url == valid_url_string

    def test_invalid_url_string_raises_exception(self, invalid_url_string):
        from logtweet._source.valid_url_string import ValidUrl
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            ValidUrl(invalid_url_string)

    def test_invalid_url_string_shown_in_raised_exception(self, invalid_url_string):
        from logtweet._source.valid_url_string import ValidUrl
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(
            NotAUrlError,
            match=r"^The given source string '{0}' is not a URL!".format(
                invalid_url_string,
            ),
        ):
            ValidUrl(invalid_url_string)
