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
        valid_url,
    ):
        mock_page_content = "<html><body>The content</body></html>"
        from logtweet._source.online import requests
        monkeypatch.setattr(
            requests,
            "get",
            self.mock_get_factory(200, mock_page_content),
        )
        from logtweet._source.online import OnlineLogSource
        online_obj = OnlineLogSource(valid_url)

        returned_page_content = online_obj.get_content_from_url(
            url=valid_url,
        )

        assert returned_page_content == mock_page_content

    def test_returns_page_content_instance_source_string_if_none_passed(
        self,
        monkeypatch,
        valid_url,
    ):
        mock_page_content = "<html><body>The content</body></html>"
        from logtweet._source.online import requests
        monkeypatch.setattr(
            requests,
            "get",
            self.mock_get_factory(200, mock_page_content),
        )
        from logtweet._source.online import OnlineLogSource
        online_obj = OnlineLogSource(valid_url)

        returned_page_content = online_obj.get_content_from_url()

        assert returned_page_content == mock_page_content

    def test_raises_error_for_404(
        self,
        monkeypatch,
        valid_url,
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
        online_obj = OnlineLogSource(valid_url)

        with pytest.raises(HTTPStatusError):
            online_obj.get_content_from_url()

    def test_error_for_404_shows_status_code(
        self,
        monkeypatch,
        valid_url,
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
        online_obj = OnlineLogSource(valid_url)

        with pytest.raises(HTTPStatusError, match=r".*404.*"):
            online_obj.get_content_from_url()

    def test_raises_error_for_connection_error(self, monkeypatch, valid_url):
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
        online_obj = OnlineLogSource(valid_url)

        with pytest.raises(RequestError):
            online_obj.get_content_from_url()

    def test_raised_error_for_connection_error_shows_url(
        self,
        monkeypatch,
        valid_url,
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
        online_obj = OnlineLogSource(valid_url)

        with pytest.raises(RequestError, match=r".*{0}.*".format(valid_url)):
            online_obj.get_content_from_url()
