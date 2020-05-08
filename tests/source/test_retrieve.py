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

    def test_passing_retriever_class_raises_type_error(self) -> None:
        """
        Passing retriever class (instead of instance) raises type error.

        """
        log_content = "Just some sting that represents the content of the log."
        from logtweet.source.retrieve import AbstractSourceContentRetriever

        class MockSourceContentRetriever(AbstractSourceContentRetriever):
            def get_content(self) -> str:
                return log_content

        from logtweet.source.retrieve import get_log_content_from_source

        with pytest.raises(TypeError):
            get_log_content_from_source(
                MockSourceContentRetriever,  # type: ignore
            )

    def test_not_inherited_retrievers_raise_type_error(self) -> None:
        """
        Retrievers not inherited from the abstract class raise type error.

        """
        class MockSourceContentRetriever(object):
            def get_content(self) -> str:
                return "some string"
        mock_source_content_retriever = MockSourceContentRetriever()
        from logtweet.source.retrieve import get_log_content_from_source

        with pytest.raises(TypeError):
            get_log_content_from_source(
                mock_source_content_retriever,  # type: ignore
            )

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
