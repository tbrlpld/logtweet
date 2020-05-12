# -*- coding: utf-8 -*-

"""Tests for the OnlineSourceRetriever class."""

import pytest  # type: ignore


# TEST: Mock actually available online server. So run an HTTP server for the
#       test. Python comes with the simple `http.server` module that allows
#       just that.



class TestOnlineSourceRetrieverClass(object):
    """Tests for the ``OnlineSourceRetriever`` class."""

    def test_subclass(self):
        """OnlineSourceRetriever is subclass of AbstractSourceRetriever."""
        from logtweet.source.retrieve import AbstractSourceContentRetriever
        from logtweet.source.online import OnlineSourceContentRetriever

        assert issubclass(
            OnlineSourceContentRetriever,
            AbstractSourceContentRetriever,
        )


class TestOnlineSourceRetrieverInit(object):
    """Test the `init` method of the `OnlineSourceContentRetriever`."""

    def test_type_error_if_init_input_wrong_type(self):
        """Raise TypeError if init input parameter not right type."""
        class NotTheRightType(object):
            pass
        wrong_type_input = NotTheRightType()
        from logtweet.source.online import OnlineSourceContentRetriever

        with pytest.raises(
            TypeError,
            match=r"Expected .*, got .*",
        ):
            OnlineSourceContentRetriever(wrong_type_input)


    # def test_valid_url_creates_instance(
    #     self,
    #     page_content,
    #     monkeypatch,
    #     valid_url,
    # ):
    #     from logtweet._source import online
    #     def returns_page_content(*args, **kwargs):
    #         return page_content
    #     monkeypatch.setattr(
    #         online,
    #         "get_content_from_url",
    #         returns_page_content,
    #     )

    #     instance = online.OnlineLogSource(valid_url)

    #     assert isinstance(instance, online.OnlineLogSource)

    # def test_valid_url_makes_content_available(
    #     self,
    #     page_content,
    #     monkeypatch,
    #     valid_url,
    # ):
    #     from logtweet._source import online
    #     def returns_page_content(*args, **kwargs):
    #         return page_content
    #     monkeypatch.setattr(
    #         online,
    #         "get_content_from_url",
    #         returns_page_content,
    #     )

    #     online_obj = online.OnlineLogSource(valid_url)

    #     assert online_obj.content == page_content

    # def test_invalid_url_raises_exception(self, invalid_url):
    #     from logtweet._source.online import OnlineLogSource
    #     from logtweet._source.exceptions import NotAUrlError

    #     with pytest.raises(NotAUrlError):
    #         OnlineLogSource(invalid_url)


# class TestGetContentFromOnlineSource(object):
#     """Test `get_content_from_online_source` static method."""

#     @staticmethod
#     def mock_get_factory(status_code: int, page_content: str = ""):
#         import requests
#         def mock_get(*args, **kwargs):
#             mock_resp = requests.Response()
#             mock_resp.status_code = status_code
#             mock_resp._content = bytes(page_content, encoding="utf-8")
#             return mock_resp
#         return mock_get

#     def test_returns_page_content_from_passed_source_string(
#         self,
#         monkeypatch,
#         valid_url_obj,
#     ):
#         mock_page_content = "<html><body>The content</body></html>"
#         from logtweet._source.online import requests
#         monkeypatch.setattr(
#             requests,
#             "get",
#             self.mock_get_factory(200, mock_page_content),
#         )
#         from logtweet._source.online import get_content_from_url

#         returned_page_content = get_content_from_url(
#             valid_url_obj,
#         )

#         assert returned_page_content == mock_page_content

#     def test_raises_error_for_404(
#         self,
#         monkeypatch,
#         valid_url_obj,
#     ):
#         mock_page_content = "<html><body>The content</body></html>"
#         from logtweet._source.online import requests
#         monkeypatch.setattr(
#             requests,
#             "get",
#             self.mock_get_factory(404, mock_page_content),
#         )
#         from logtweet._source.exceptions import HTTPStatusError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(HTTPStatusError):
#             get_content_from_url(valid_url_obj)

#     def test_error_for_404_shows_status_code(
#         self,
#         monkeypatch,
#         valid_url_obj,
#     ):
#         mock_page_content = "<html><body>The content</body></html>"
#         from logtweet._source.online import requests
#         monkeypatch.setattr(
#             requests,
#             "get",
#             self.mock_get_factory(404, mock_page_content),
#         )
#         from logtweet._source.exceptions import HTTPStatusError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(HTTPStatusError, match=r".*404.*"):
#             get_content_from_url(valid_url_obj)

#     def test_raises_error_for_connection_error(self, monkeypatch, valid_url_obj):
#         from logtweet._source.online import requests
#         def mock_get_raises_connection_error(*args, **kwargs):
#             raise requests.ConnectionError
#         monkeypatch.setattr(
#             requests,
#             "get",
#             mock_get_raises_connection_error,
#         )
#         from logtweet._source.exceptions import RequestError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(RequestError):
#             get_content_from_url(valid_url_obj)

#     def test_raised_error_for_connection_error_shows_url(
#         self,
#         monkeypatch,
#         valid_url,
#         valid_url_obj,
#     ):
#         from logtweet._source.online import requests
#         def mock_get_raises_connection_error(*args, **kwargs):
#             raise requests.ConnectionError
#         monkeypatch.setattr(
#             requests,
#             "get",
#             mock_get_raises_connection_error,
#         )
#         from logtweet._source.exceptions import RequestError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(
#             RequestError,
#             match=r".*{0}.*".format(valid_url),
#         ):
#             get_content_from_url(valid_url_obj)

#     def test_raises_type_error_if_input_not_valid_url_instance(
#         self,
#         valid_url,
#     ):
#         """
#         Test raises type error if input is not instance of  ``ValidUrl``.

#         E.g. if the input is of type string (even if this represents a valid
#         URL) the type error is raised. The caller is expected to validate the
#         URL by creating a corresponding object.

#         """
#         from logtweet._source.online import get_content_from_url
#         assert isinstance(valid_url, str)

#         with pytest.raises(TypeError):
#             get_content_from_url(valid_url)

