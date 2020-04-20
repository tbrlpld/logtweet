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
def valid_url_obj(valid_url):
    from logtweet._source.valid_url import ValidUrl
    return ValidUrl(valid_url)


@pytest.fixture
def invalid_url():
    return "not a url, just a string"


@pytest.fixture
def page_content():
    return "<html><body>The content</body></html>"


class TestGetContentFromOnlineSource(object):
    """Test `get_content_from_online_source` static method."""

    @staticmethod
    def mock_get_factory(status_code: int, page_content: str = ""):
        import requests
        def mock_get(*args, **kwargs):
            mock_resp = requests.Response()
            mock_resp.status_code = status_code
            mock_resp._content = bytes(page_content, encoding="utf-8")
            return mock_resp
        return mock_get

    def test_returns_page_content_from_passed_source_string(
        self,
        monkeypatch,
        valid_url_obj,
    ):
        mock_page_content = "<html><body>The content</body></html>"
        from logtweet._source.online import requests
        monkeypatch.setattr(
            requests,
            "get",
            self.mock_get_factory(200, mock_page_content),
        )
        from logtweet._source.online import OnlineLogSource

        returned_page_content = OnlineLogSource.get_content_from_url(
            valid_url_obj,
        )

        assert returned_page_content == mock_page_content

    def test_raises_error_for_404(
        self,
        monkeypatch,
        valid_url_obj,
    ):
        mock_page_content = "<html><body>The content</body></html>"
        from logtweet._source.online import requests
        monkeypatch.setattr(
            requests,
            "get",
            self.mock_get_factory(404, mock_page_content),
        )
        from logtweet._source.exceptions import HTTPStatusError
        from logtweet._source.online import OnlineLogSource

        with pytest.raises(HTTPStatusError):
            OnlineLogSource.get_content_from_url(valid_url_obj)

    def test_error_for_404_shows_status_code(
        self,
        monkeypatch,
        valid_url_obj,
    ):
        mock_page_content = "<html><body>The content</body></html>"
        from logtweet._source.online import requests
        monkeypatch.setattr(
            requests,
            "get",
            self.mock_get_factory(404, mock_page_content),
        )
        from logtweet._source.exceptions import HTTPStatusError
        from logtweet._source.online import OnlineLogSource

        with pytest.raises(HTTPStatusError, match=r".*404.*"):
            OnlineLogSource.get_content_from_url(valid_url_obj)

    def test_raises_error_for_connection_error(self, monkeypatch, valid_url_obj):
        from logtweet._source.online import requests
        def mock_get_raises_connection_error(*args, **kwargs):
            raise requests.ConnectionError
        monkeypatch.setattr(
            requests,
            "get",
            mock_get_raises_connection_error,
        )
        from logtweet._source.exceptions import RequestError
        from logtweet._source.online import OnlineLogSource

        with pytest.raises(RequestError):
            OnlineLogSource.get_content_from_url(valid_url_obj)

    def test_raised_error_for_connection_error_shows_url(
        self,
        monkeypatch,
        valid_url,
        valid_url_obj,
    ):
        from logtweet._source.online import requests
        def mock_get_raises_connection_error(*args, **kwargs):
            raise requests.ConnectionError
        monkeypatch.setattr(
            requests,
            "get",
            mock_get_raises_connection_error,
        )
        from logtweet._source.exceptions import RequestError
        from logtweet._source.online import OnlineLogSource

        with pytest.raises(
            RequestError,
            match=r".*{0}.*".format(valid_url),
        ):
            OnlineLogSource.get_content_from_url(valid_url_obj)


class TestInitialization(object):
    """Test the initialization of ``OnlineLogSource``."""

    def test_valid_url_creates_instance(
        self,
        page_content,
        monkeypatch,
        valid_url,
    ):
        from logtweet._source.online import OnlineLogSource
        def returns_page_content(*args, **kwargs):
            return page_content
        monkeypatch.setattr(
            OnlineLogSource,
            "get_content_from_url",
            returns_page_content,
        )

        instance = OnlineLogSource(valid_url)

        assert isinstance(instance, OnlineLogSource)

    def test_valid_url_makes_content_available(
        self,
        page_content,
        monkeypatch,
        valid_url,
    ):
        from logtweet._source.online import OnlineLogSource
        def returns_page_content(*args, **kwargs):
            return page_content
        monkeypatch.setattr(
            OnlineLogSource,
            "get_content_from_url",
            returns_page_content,
        )

        online_obj = OnlineLogSource(valid_url)

        assert online_obj.content == page_content

    def test_invalid_url_raises_exception(self, invalid_url):
        from logtweet._source.online import OnlineLogSource
        from logtweet._source.exceptions import NotAUrlError

        with pytest.raises(NotAUrlError):
            OnlineLogSource(invalid_url)

