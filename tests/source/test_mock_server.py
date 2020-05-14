# -*- coding: utf-8 -*-

"""Test the functionality of the mock server."""

import typing


if typing.TYPE_CHECKING:
    from http import server as httpserver


class TestMockServer(object):
    """Verify that defined test server works."""

    def test_mock_server(
        self,
        request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]],
        mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
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
