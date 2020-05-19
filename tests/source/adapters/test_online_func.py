# -*- coding: utf-8 -*-

"""
Functional tests for the OnlineSourceRetriever class.

"""

import typing

import pytest  # type: ignore


if typing.TYPE_CHECKING:
    from http import server as httpserver
    from logtweet.source.adapters import onlineretriever as adaptonline


class TestOnlineSourceContentRetrieverGetContentFunctional(object):
    """
    Functional tests for the `get_content` method.

    These tests create a mock web server that can be reached instead of mocking
    the internally used function (like `requests.get`). This makes these tests
    more valuable, because they actually test the implementation.
    """

    def test_sucessful_content_retrieval(
        self,
        request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]],
        mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
        valid_online_source_factory: typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"],
    ) -> None:
        """Content from mock server is returned."""
        defined_content = "The content"
        defined_status_code = 200
        request_handler = request_get_handler_class_factory(
            defined_status_code,
            defined_content,
        )
        mock_server = mock_server_factory(request_handler)
        source_string = "http://{0}:{1}/".format(mock_server[0], mock_server[1])
        # Create a valid online source without actually validating
        valid_online_source = valid_online_source_factory(source_string)
        from logtweet.source.adapters import onlineretriever as adaptonline
        online_source_content_retriever = adaptonline.OnlineSourceContentRetriever(
            valid_online_source,
        )

        actual_content = online_source_content_retriever.get_content()

        assert actual_content == defined_content

    def test_exception_if_404_response(
        self,
        request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]],
        mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
        valid_online_source_factory: typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"],
    ) -> None:
        """Raises exception when server responds with 404 status."""
        defined_status_code = 404
        request_handler = request_get_handler_class_factory(  # type: ignore
            defined_status_code,
        )
        mock_server = mock_server_factory(request_handler)
        source_string = "http://{0}:{1}/".format(mock_server[0], mock_server[1])
        # Create a valid online source without actually validating
        valid_online_source = valid_online_source_factory(source_string)
        from logtweet.source.adapters import onlineretriever as adaptonline
        online_source_content_retriever = adaptonline.OnlineSourceContentRetriever(
            valid_online_source,
        )
        from logtweet.source.adapters import onlineretriever as adaptonline

        with pytest.raises(adaptonline.HTTPStatusError):
            online_source_content_retriever.get_content()

    def test_expection_if_server_not_avilable(
        self,
        free_port: int,
        valid_online_source_factory: typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"],
    ) -> None:
        """Raises exception if server is not available."""
        source_string = "http://localhost:{0}/".format(free_port)
        # Create a valid online source without actually validating
        valid_online_source = valid_online_source_factory(source_string)
        from logtweet.source.adapters import onlineretriever as adaptonline
        online_source_content_retriever = adaptonline.OnlineSourceContentRetriever(
            valid_online_source,
        )
        from logtweet.source.adapters import onlineretriever as adaptonline

        with pytest.raises(adaptonline.RequestError):
            online_source_content_retriever.get_content()
