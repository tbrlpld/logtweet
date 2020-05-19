# -*- coding: utf-8 -*-

"""Test for the retrieve controller."""

import typing


if typing.TYPE_CHECKING:
    from http import server as httpserver
    from logtweet.source.adapters import validurl as adapturl
    from logtweet.source.adapters import onlineretriever as adaptonline


def test_exiting_url_to_content(
    request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]],
    mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
) -> None:
    """Return log content from mock server when given its URL."""
    status_code = 200
    page_content = "This is the content"
    request_get_handler = request_get_handler_class_factory(
        status_code,
        page_content,
    )
    mock_server = mock_server_factory(request_get_handler)
    url = "http://{0}:{1}".format(mock_server[0], mock_server[1])
    from logtweet.source.controllers import retrieve as ctrlretrieve

    returned_content = ctrlretrieve.get_log_content_from_source(
        source_string=url,
    )

    assert returned_content == page_content

# TEST: Returns log content from local file when given it's path
# TEST: Raises and error when source string neither path nor URL.
