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
        """Validates URL."""
        from logtweet.source.adapters.validurl import ValidSourceURL

        is_valid = ValidSourceURL.is_valid(valid_url_string)

        assert is_valid is True

    def test_localhost_is_valid(self) -> None:
        """Localhost address with port is valid."""
        url = "http://localhost:8000/"
        from logtweet.source.adapters.validurl import ValidSourceURL

        is_valid = ValidSourceURL.is_valid(url)

        assert is_valid is True

    def test_invalid_url_string(
        self,
        invalid_url_string: str,
    ) -> None:
        """Fails on non-URL string."""
        from logtweet.source.adapters.validurl import ValidSourceURL

        is_valid = ValidSourceURL.is_valid(invalid_url_string)

        assert is_valid is False


class TestValidUrlInitialization(object):
    """Test initialization of ValidURL."""

    def test_valid_url_string_creates_object(
        self,
        valid_url_string: str,
    ) -> None:
        """Init succeeds with valid url."""
        from logtweet.source.adapters.validurl import ValidSourceURL

        url_obj = ValidSourceURL(valid_url_string)

        assert isinstance(url_obj, ValidSourceURL)

    def test_valid_object_has_url_property(
        self,
        valid_url_string: str,
    ) -> None:
        """Initialized object has `url` property."""
        from logtweet.source.adapters.validurl import ValidSourceURL

        url_obj = ValidSourceURL(valid_url_string)

        assert url_obj.url == valid_url_string

    def test_invalid_url_raises_exception(
        self,
        invalid_url_string: str,
    ) -> None:
        """
        Init fails with exception on invalid URL.

        Exception contains passed string that is not a URL.

        """
        from logtweet.source.usecases.retrieve import SourceValidationError
        from logtweet.source.adapters.validurl import ValidSourceURL

        with pytest.raises(
            SourceValidationError,
            match=r".*{0}.*".format(invalid_url_string),
        ):
            ValidSourceURL(invalid_url_string)
