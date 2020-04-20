# -*- coding: utf-8 -*-

"""Tests for the OnlineLogSource class."""

import pytest  # type: ignore


# Tests for reaching an online source require a working online connection.
# Or I need to mock the function that represents the availability of an online
# source.
@pytest.fixture
def valid_url():
    return "https://example.com"


@pytest.fixture
def invalid_url():
    return "not a url, just a string"


class TestInitialization(object):
    """Test the initialization of ``OnlineLogSource``."""
    def test_valid_url_creates_instance(self, valid_url):
        from logtweet._source.online import OnlineLogSource

        instance = OnlineLogSource(valid_url)

        assert isinstance(instance, OnlineLogSource)

    def test_invalid_url_raises_exception(self, invalid_url):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            OnlineLogSource(invalid_url)


class TestRaiseForInvalidUrlStaticMethod(object):
    """Test the static ``raise_for_invalid_url`` method."""

    def test_valid_url_returns_none(self, valid_url):
        from logtweet._source.online import OnlineLogSource

        is_valid = OnlineLogSource.raise_for_invalid_url(valid_url)

        assert is_valid is None

    def test_invalid_url_raises_exception(self, invalid_url):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            OnlineLogSource.raise_for_invalid_url(invalid_url)

    def test_invalid_url_shown_in_raised_exception(self, invalid_url):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(
            NotAUrlError,
            match=r"^The given source string '{0}' is not a URL!".format(
                invalid_url,
            ),
        ):
            OnlineLogSource.raise_for_invalid_url(invalid_url)


class TestGetContentFromOnlineSource(object):
    """Test `get_content_from_online_source` method."""

    def test_returns_page_content_from_source_string(
        self,
        monkeypatch,
        valid_url,
    ):
        mock_page_content = "<html><body>The content</body></html>"
        from logtweet._source.online import requests
        def mock_get(*args, **kwargs):
            mock_resp = requests.Response()
            mock_resp.status = 200
            mock_resp._content = bytes(mock_page_content, encoding="utf-8")
            return mock_resp
        monkeypatch.setattr(requests, "get", mock_get)
        from logtweet._source.online import OnlineLogSource
        online_obj = OnlineLogSource(valid_url)

        returned_page_content = online_obj.get_content_from_online_source(
            source_string=valid_url,
        )

        assert returned_page_content == mock_page_content
