# -*- coding: utf-8 -*-

"""Tests for the content retrieval use case "get log content from source"."""


import pytest  # type: ignore


class TestGetLogContentFromSource(object):
    """Test the `get_log_content_from_source` function."""

    def test_return_content_from_mock_source_content_retriever(
        self,
    ) -> None:
        """
        Use case returns content from source instance.

        Also tests the existence of the AbstractSource class.

        """
        log_content = "Just some sting that represents the content of the log."
        from logtweet.source.retrieve import AbstractSourceContentRetriever

        class MockSourceContentRetriever(AbstractSourceContentRetriever):
            def get_content(self) -> str:
                return log_content
        mock_source_content_retriever = MockSourceContentRetriever()
        from logtweet.source.retrieve import get_log_content_from_source

        returned_content = get_log_content_from_source(
            mock_source_content_retriever,
        )

        assert returned_content == log_content

    # TEST: Retrievers that inherited from the abstract class are not accepted.

    def test_exception_during_content_retrieval_not_caught(
        self,
    ) -> None:
        """An exception raised during content retrieval is not caught."""
        class TestExceptionError(Exception):
            pass

        from logtweet.source.retrieve import AbstractSourceContentRetriever
        class MockSourceContentRetriever(AbstractSourceContentRetriever):
            def get_content(self) -> str:
                raise TestExceptionError
        mock_source_content_retriever = MockSourceContentRetriever()
        from logtweet.source.retrieve import get_log_content_from_source

        with pytest.raises(TestExceptionError):
            get_log_content_from_source(
                mock_source_content_retriever,
            )


    # def test_invalid_url_raises_exception(
    #     self,
    #     invalid_url,
    # ):
    #     """
    #     Test invalid URL raises exception.

    #     I am not testing for any specific exceptions, because that is up to the
    #     implementation, i.e. depends on the lower level functions.

    #     """
    #     from logtweet.source import get_log_content_from_source

    #     with pytest.raises(Exception):
    #         get_log_content_from_source(invalid_url)


# class TestAbstactSource(object):

#     def test_import(self):
#         from logtweet.source.content_retrival import AbstractSource
