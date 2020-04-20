# -*- coding: utf-8 -*-

"""Tests for the OnlineLogSource class."""

import pytest  # type: ignore

@pytest.fixture
def valid_url():
    return "https://example.com"


@pytest.fixture
def invalid_url():
    return "not a url, just a string"


class TestIsValidUrlStaticMethod(object):
    """Test the static ``raise_for_invalid_url`` method."""

    def test_valid_url_returns_none(self, valid_url):
        from logtweet._source.valid_url import ValidUrl

        is_valid = ValidUrl.is_valid_url(valid_url)

        assert is_valid is True

    def test_valid_url_returns_none(self, invalid_url):
        from logtweet._source.valid_url import ValidUrl

        is_valid = ValidUrl.is_valid_url(invalid_url)

        assert is_valid is False


class TestValidUrlInitialization(object):
    """Test initialization of ValidURL."""

    def test_valid_url_creates_object(self, valid_url):
        from logtweet._source.valid_url import ValidUrl

        url_obj = ValidUrl(valid_url)

        assert isinstance(url_obj, ValidUrl)

    def test_valid_object_has_url_property(self, valid_url):
        from logtweet._source.valid_url import ValidUrl

        url_obj = ValidUrl(valid_url)

        assert url_obj.url == valid_url

    def test_invalid_url_raises_exception(self, invalid_url):
        from logtweet._source.valid_url import ValidUrl
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            ValidUrl(invalid_url)

    def test_invalid_url_shown_in_raised_exception(self, invalid_url):
        from logtweet._source.valid_url import ValidUrl
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(
            NotAUrlError,
            match=r"^The given source string '{0}' is not a URL!".format(
                invalid_url,
            ),
        ):
            ValidUrl(invalid_url)
