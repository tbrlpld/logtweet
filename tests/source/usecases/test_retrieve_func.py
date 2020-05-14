# -*- coding: utf-8 -*-

"""Functional black box tests for the retrieval usecase."""

import typing

import pytest  # type: ignore

if typing.TYPE_CHECKING:
    from http import server as httpserver
    from logtweet.source.adapters import onlineretriever as adaptonline


@pytest.fixture  # type: ignore
def online_source_retriever_for_mock_server_factory(
    request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]],
    mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
    valid_online_source_factory: typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"],
) -> typing.Callable[[int, str], "adaptonline.OnlineSourceContentRetriever"]:
    """
    Return factory function for valid online source object for running mock server.

    This is only the fixture that returns the actual factory function.

    Parameters
    ----------
    request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]]
        Fixture returning a factory function to create simple request handlers.
    mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
        Fixture returning a factory function to create a running webserver.
    valid_online_source_factory: typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"],
        Fixture returning a factory function to create a valid online source
        object for a given `url`.

    Returns
    -------
    typing.Callable[[int, str], "adaptonline.OnlineSourceContentRetriever"]
        Factory function to create a valid online source object representing
        the running mock websever. The mock server's url is available on the
        returned object in the `url` property.

    """
    from logtweet.source.adapters import onlineretriever as adaptonline

    def actual_factory(
        status_code: int,
        page_content: str,
    ) -> "adaptonline.OnlineSourceContentRetriever":
        """
        Create a valid online source object for the running mock websever.

        The mock server's url is available on the returned object in the `url`
        property.

        Parameters
        ----------
        status_code: int
            Status code that the mock web server is responding with to the
            requests.
        page_content: str
            Page content that the mock web server is responding with to the
            requests.

        Returns
        -------
        adaptonline.OnlineSourceContentRetriever
            OnlineSourceContentRetriever instance, configure to retrieve
            content from the mock server.

        """
        request_get_handler = request_get_handler_class_factory(
            status_code,
            page_content,
        )
        mock_server = mock_server_factory(request_get_handler)
        url = "http://{0}:{1}/".format(mock_server[0], mock_server[1])
        valid_online_source = valid_online_source_factory(url)
        return adaptonline.OnlineSourceContentRetriever(valid_online_source)

    return actual_factory


class TestGetLogContentFromSource(object):

    def test_returns_content_from_online_source(
        self,
        online_source_retriever_for_mock_server_factory: typing.Callable[[int, str], "adaptonline.OnlineSourceContentRetriever"],
    ) -> None:
        defined_status_code = 200
        defined_page_content = "This is the content"
        online_source_retriever = online_source_retriever_for_mock_server_factory(
            defined_status_code,
            defined_page_content,
        )
        from logtweet.source.usecases import retrieve as ucretrieve

        returned_content = ucretrieve.get_log_content_from_source(online_source_retriever)

        assert returned_content == defined_page_content
