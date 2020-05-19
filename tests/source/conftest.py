# -*- coding: utf-8 -*-

"""
Fixtures for the source tests

Looked up how to setup a mock server here:
https://realpython.com/testing-third-party-apis-with-mock-servers/#testing-the-mock-api

"""

from http import server as httpserver
import socket
import threading
import typing

import pytest  # type: ignore

if typing.TYPE_CHECKING:
    from logtweet.source.adapters import onlineretriever as adaptonline


@pytest.fixture  # type: ignore
def valid_online_source_factory(
) -> typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"]:
    """
    Create factory function to create `adaptonline.AbstractValidOnlineSource` instance.

    Returns
    -------
    typing.Callable[[str], "adaptonline.AbstractValidOnlineSource"]
        Factory function to create instances of a subclass of
        `adaptonline.AbstractValidOnlineSource`.

    """
    from logtweet.source.adapters import onlineretriever as adaptonline

    def valid_online_source(source_string: str) -> adaptonline.AbstractValidOnlineSource:
        """
        Create instance of `adaptonline.AbstractValidOnlineSource` subclass.

        Accepts a `source_string` parameter and returns an instance of subclass
        of `AbstractVaildOnlineSource`.

        No validation is actually performed. The `is_valid` method of the
        subclass always returns `True`.

        The `source_string` value will be available on returned object in the
        `url` property.

        Parameters
        ----------
        source_string : str
            Source string to assign to the `url` property of the returned
            instance of the `adaptonline.AbstractValidOnlineSource` subclass.

        Returns
        -------
        adaptonline.AbstractValidOnlineSource
            Instance of an internal subclass of `adaptonline.AbstractValidOnlineSource`.
            The object will have the given `source_string` available as its
            `url` property.

        """

        class ValidOnlineSourceForTest(adaptonline.AbstractValidOnlineSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True

        return ValidOnlineSourceForTest(source_string)

    return valid_online_source


@pytest.fixture  # type: ignore
def request_get_handler_class_factory(
) -> typing.Callable[[int, str], typing.Type[httpserver.BaseHTTPRequestHandler]]:
    """
    Return factory function to create get request handlers.

    Returns
    -------
    typing.Callable[[int, str], typing.Type[httpserver.BaseHTTPRequestHandler]]
        Factory function to create get request handlers.

    """

    def concrete_get_handler_class_factory(
        status_code: int,
        body: str = "",
    ) -> typing.Type[httpserver.BaseHTTPRequestHandler]:
        """
        Create get request handler.

        Parameters
        ----------
        status_code : int
            Status code with which the handler is responding.
        body : str
            Response body (this is where the HTML would go).

        Returns
        -------
        httpserver.BaseHTTPRequestHandler
            Subclass of the `httpserver.BaseHTTPRequestHandler` which responds with the
            defined status code and body.

        """
        class MockServerRequestHandler(httpserver.BaseHTTPRequestHandler):
            """Mock request handler for the mock server."""

            def do_GET(self) -> None:
                """Return response to HTTP GET request."""
                self.send_response(status_code)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                if body:
                    self.wfile.write(body.encode("utf-8"))
        return MockServerRequestHandler

    return concrete_get_handler_class_factory


@pytest.fixture  # type: ignore
def free_port() -> int:
    """
    Return free port on the localhost.

    Returns
    -------
    int
        Free port number on the localhost.

    """
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port: int
    _, port = sock.getsockname()
    sock.close()
    return port


@pytest.fixture  # type: ignore
def mock_server_factory(
    free_port: int,
) -> typing.Callable[[typing.Type[httpserver.BaseHTTPRequestHandler]], typing.Tuple[str, int]]:
    """
    Return factory func that creates a web server with a given request handler.

    Parameters
    ----------
    free_port : int
        Free port on the localhost on which to bind the web servers created by
        the returned factory function.

    Returns
    -------
    typing.Callable[[typing.Type[httpserver.BaseHTTPRequestHandler]], typing.Tuple[str, int]]
        Factory function to create a web server from a given request handler.

    """

    def concrete_server_factory(
        request_handler_class: typing.Type[httpserver.BaseHTTPRequestHandler],
    ) -> typing.Tuple[str, int]:
        """
        Create web server with given request handler.

        The web server is also started automatically in a thread. The thread
        automatically stops when the parent stops.

        Parameters
        ----------
        request_handler_class: typing.Type[httpserver.BaseHTTPRequestHandler]
            Request handler which handles the requests send to the web server.

        Returns
        -------
        typing.Tuple[str, int]
            typing.Tuple containing the servers domain ("localhost") and the port it
            is listening on.

        """
        mock_server_domain = "localhost"
        mock_server_port = free_port
        mock_server = httpserver.HTTPServer(
            (mock_server_domain, mock_server_port),
            request_handler_class,
        )

        mock_server_thread = threading.Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()

        return mock_server_domain, mock_server_port

    return concrete_server_factory
