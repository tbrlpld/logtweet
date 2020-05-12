# -*- coding: utf-8 -*-

"""
Functional tests for the OnlineSourceRetriever class.

Looked up how to setup a mock server here:
https://realpython.com/testing-third-party-apis-with-mock-servers/#testing-the-mock-api

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
from typing import Callable, Tuple, Type

import pytest  # type: ignore


# TEST: (1) Mock actually available online server. So run an HTTP server for the
#       test. Python comes with the simple `http.server` module that allows
#       just that.


@pytest.fixture  # type: ignore
def request_get_handler_class_factory(
) -> Callable[[int, str], Type[BaseHTTPRequestHandler]]:
    """
    Return factory function to create get request handlers.

    Returns
    -------
    Callable[[int, str], Type[BaseHTTPRequestHandler]]
        Factory function to create get request handlers.

    """

    def concrete_get_handler_class_factory(
        status_code: int,
        body: str = "",
    ) -> Type[BaseHTTPRequestHandler]:
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
        BaseHTTPRequestHandler
            Subclass of the `BaseHTTPRequestHandler` which responds with the
            defined status code and body.

        """
        class MockServerRequestHandler(BaseHTTPRequestHandler):
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
) -> Callable[[Type[BaseHTTPRequestHandler]], Tuple[str, int]]:
    """
    Return factory func that creates a web server with a given request handler.

    Parameters
    ----------
    free_port : int
        Free port on the localhost on which to bind the web servers created by
        the returned factory function.

    Returns
    -------
    Callable[[Type[BaseHTTPRequestHandler]], Tuple[str, int]]
        Factory function to create a web server from a given request handler.

    """

    def concrete_server_factory(
        request_handler_class: Type[BaseHTTPRequestHandler],
    ) -> Tuple[str, int]:
        """
        Create web server with given request handler.

        The web server is also started automatically in a thread. The thread
        automatically stops when the parent stops.

        Parameters
        ----------
        request_handler_class: Type[BaseHTTPRequestHandler]
            Request handler which handles the requests send to the web server.

        Returns
        -------
        Tuple[str, int]
            Tuple containing the servers domain ("localhost") and the port it
            is listening on.

        """
        mock_server_domain = "localhost"
        mock_server_port = free_port
        mock_server = HTTPServer(
            (mock_server_domain, mock_server_port),
            request_handler_class,
        )

        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()

        return mock_server_domain, mock_server_port

    return concrete_server_factory


class TestMockServer(object):
    """Verify that defined test server works."""

    def test_mock_server(
        self,
        request_get_handler_class_factory: Callable[[int, str], Type[BaseHTTPRequestHandler]],
        mock_server_factory: Callable[[Type[BaseHTTPRequestHandler]], Tuple[str, int]],
    ) -> None:
        """Verify that defined test server works."""
        defined_content = "The content"
        defined_status_code = 200
        request_handler = request_get_handler_class_factory(
            defined_status_code,
            defined_content,
        )
        mock_server = mock_server_factory(request_handler)
        url = "http://{0}:{1}/".format(mock_server[0], mock_server[1])
        import requests

        response = requests.get(url)

        assert response.status_code == 200
        assert response.text == "The content"
