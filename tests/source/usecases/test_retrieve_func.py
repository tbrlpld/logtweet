# -*- coding: utf-8 -*-

"""Functional black box tests for the retrieval usecase."""

import typing

import pytest  # type: ignore

if typing.TYPE_CHECKING:
    from http import server as httpserver
    from logtweet.source.adapters import validurl as adapturl
    from logtweet.source.adapters import onlineretriever as adaptonline


class TestGetLogContentFromOnlineSource(object):
    """
    Functionally test usecase `get_log_contente_from_source` for online source.

    """

    @pytest.fixture  # type: ignore
    def online_source_retriever_for_mock_server_factory(
        self,
        request_get_handler_class_factory: typing.Callable[[int, str], typing.Type["httpserver.BaseHTTPRequestHandler"]],
        mock_server_factory: typing.Callable[[typing.Type["httpserver.BaseHTTPRequestHandler"]], typing.Tuple[str, int]],
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

        Returns
        -------
        typing.Callable[[int, str], "adaptonline.OnlineSourceContentRetriever"]
            Factory function to create a valid online source object representing
            the running mock websever. The mock server's url is available on the
            returned object in the `url` property.

        """
        from logtweet.source.adapters import validurl as adapturl
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
            validurl = adapturl.ValidSourceURL(url)
            return adaptonline.OnlineSourceContentRetriever(validurl)

        return actual_factory

    def test_returns_content_from_online_source(
        self,
        online_source_retriever_for_mock_server_factory: typing.Callable[[int, str], "adaptonline.OnlineSourceContentRetriever"],
    ) -> None:
        """
        Returns page content for online source retriever.
        """
        defined_status_code = 200
        defined_page_content = "This is the content"
        online_source_retriever = online_source_retriever_for_mock_server_factory(
            defined_status_code,
            defined_page_content,
        )
        from logtweet.source.usecases import retrieve as ucretrieve

        returned_content = ucretrieve.get_log_content_from_source(
            online_source_retriever,
        )

        assert returned_content == defined_page_content

    def test_exception_when_404_response(
        self,
        online_source_retriever_for_mock_server_factory: typing.Callable[[int, str], "adaptonline.OnlineSourceContentRetriever"],
    ) -> None:
        defined_status_code = 404
        defined_page_content = "This is the content"
        online_source_retriever = online_source_retriever_for_mock_server_factory(
            defined_status_code,
            defined_page_content,
        )
        from logtweet.source.usecases import retrieve as ucretrieve

        with pytest.raises(
            ucretrieve.SourceContentRetrievalError,
            match=r".*404.*",
        ):
            ucretrieve.get_log_content_from_source(online_source_retriever)

    def test_exception_when_server_not_available(
        self,
        free_port: int,
    ) -> None:
        url = "http://localhost:{0}".format(free_port)
        from logtweet.source.adapters import validurl as adapturl
        from logtweet.source.adapters import onlineretriever as adaptonline
        validurl = adapturl.ValidSourceURL(url)
        online_source_retriever = adaptonline.OnlineSourceContentRetriever(
            validurl,
        )
        from logtweet.source.usecases import retrieve as ucretrieve

        with pytest.raises(ucretrieve.SourceContentRetrievalError):
            ucretrieve.get_log_content_from_source(online_source_retriever)

