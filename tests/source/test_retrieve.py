# -*- coding: utf-8 -*-

"""Tests for the content retrieval use case "get log content from source"."""


import pytest  # type: ignore


class TestAbstractValidSource(object):
    """Test `AbstractValidSource` class."""

    def test_child_init_succeeds_if_is_valid(self) -> None:
        """
        Child init succeeds if `is_valid` is `True`.

        If the implementation of `is_valid` succeeds, then the initialization
        of the valid source will succeed.

        """
        from logtweet.source.retrieve import AbstractValidSource
        class Child(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True

        Child("some_string")

    def test_source_string_property_on_instance(self) -> None:
        """Source string available on initialized child."""
        source_string = "some source string"
        from logtweet.source.retrieve import AbstractValidSource
        class Child(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True

        child_instance = Child(source_string)

        assert child_instance.source_string == source_string

    def test_raise_validation_error_if_not_is_valid(self) -> None:
        """Raise SourceValidationError if `is_valid` returns False."""
        from logtweet.source.retrieve import (
            AbstractValidSource,
            SourceValidationError,
        )
        class Child(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return False

        with pytest.raises(SourceValidationError):
            Child("some_string")

    def test_child_init_argument_is_string(self) -> None:
        """
        `source_string` argument of init is string.

        Raise TypeError if not.

        """
        class WrongType(object):
            pass
        wrong_typed_argument = WrongType()

        from logtweet.source.retrieve import AbstractValidSource
        class Child(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True

        with pytest.raises(
            TypeError,
            match=r"Expected str, got .*",
        ):
            Child(wrong_typed_argument)  # type: ignore

    def test_child_init_requires_source_sting_argument(self) -> None:
        """
        Child init requires source string.

        If the argument is not passed, an exception is raised.

        """
        from logtweet.source.retrieve import AbstractValidSource
        class Child(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True

        with pytest.raises(
            TypeError,
            match=r".*missing.*argument",
        ):
            Child()  # type: ignore

    def test_is_valid_requires_source_string_argument(self) -> None:
        """
        `is_valid` requires source string argument.

        If the argument is not passed, an exception is raised.

        """
        from logtweet.source.retrieve import AbstractValidSource

        with pytest.raises(
            TypeError,
            match=r".*missing.*argument",
        ):
            AbstractValidSource.is_valid()  # type: ignore

    def test_child_init_fails_if_is_valid_not_implemented(self) -> None:
        """
        Child init fails if is_valid not implemented.

        `is_valid` is the one abstract method that is required.

        """
        from logtweet.source.retrieve import AbstractValidSource
        class Child(AbstractValidSource):
            def __init__(self) -> None:
                pass

        with pytest.raises(
            TypeError,
            match=r"Can't instantiate.*abstract",
        ):
            Child()  # type: ignore

    def test_direct_init_fails(self) -> None:
        """Direct init fails."""
        from logtweet.source.retrieve import AbstractValidSource

        with pytest.raises(
            TypeError,
            match=r"Can't instantiate.*abstract",
        ):
            AbstractValidSource()  # type: ignore


class TestAbstactSourceContentRetriever(object):
    """Test `AbstractSourceContentRetriever` class."""

    def test_instantiation_succeeds(self) -> None:
        """Successful instantiation."""
        from logtweet.source.retrieve import AbstractValidSource
        class ValidTestSource(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True
        valid_test_source = ValidTestSource("some string")
        from logtweet.source.retrieve import AbstractSourceContentRetriever
        class SourceContentRetrieverImplementation(
            AbstractSourceContentRetriever,
        ):
            def get_content(self) -> str:
                return ""

        SourceContentRetrieverImplementation(
            valid_test_source,
        )

    def test_source_property_available_on_instance(self) -> None:
        """Source property available on instance."""
        from logtweet.source.retrieve import AbstractValidSource
        class ValidTestSource(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True
        valid_test_source = ValidTestSource("some string")
        from logtweet.source.retrieve import AbstractSourceContentRetriever
        class SourceContentRetrieverImplementation(
            AbstractSourceContentRetriever,
        ):
            def get_content(self) -> str:
                return ""

        source_content_retriever = SourceContentRetrieverImplementation(
            valid_test_source,
        )

        assert source_content_retriever.valid_source == valid_test_source

    # TEST: SourceContentRetrivalError is available to be raised in `get_content` implementation

    def test_instantiaing_child_fails_if_not_passed_valid_source_type(
        self,
    ) -> None:
        """
        Instantiating child fails if source argument not correct type.

        Only instances of subclasses of `AbstractValidSource` are accepted.

        """
        class NotValidSourceType(object):
            pass
        from logtweet.source.retrieve import AbstractSourceContentRetriever
        class Child(AbstractSourceContentRetriever):
            def get_content(self) -> str:
                return ""

        with pytest.raises(
            TypeError,
            match=r"Expected.* got.*",
        ):
            Child(NotValidSourceType())  # type: ignore

    def test_instantiating_child_fails_if_not_passed_valid_source_instance(
        self,
    ) -> None:
        """Instantiation of child requires validated source instance."""
        from logtweet.source.retrieve import AbstractSourceContentRetriever

        class Child(AbstractSourceContentRetriever):
            def get_content(self) -> str:
                return ""

        with pytest.raises(
            TypeError,
            match=r".*missing.*argument.*",
        ):
            Child()  # type: ignore

    def test_instantiating_child_fails_if_not_implements_get_content_method(
        self,
    ) -> None:
        """Instantiation of child fails if not implements `get_content`."""
        from logtweet.source.retrieve import AbstractSourceContentRetriever

        class Child(AbstractSourceContentRetriever):
            pass

        with pytest.raises(
            TypeError,
            match=r"Can't instantiate",
        ):
            Child()  # type: ignore

    def test_direct_instantiation_fails(self) -> None:
        """Direct instantiation fails."""
        from logtweet.source.retrieve import AbstractSourceContentRetriever

        with pytest.raises(
            TypeError,
            match=r"Can't instantiate",
        ):
            AbstractSourceContentRetriever()  # type: ignore


class TestGetLogContentFromSource(object):
    """Test the `get_log_content_from_source` function."""

    # Import for type annotations
    from logtweet.source.retrieve import AbstractValidSource

    @pytest.fixture  # type: ignore
    def mock_valid_source(
        self,
    ) -> AbstractValidSource:
        """
        Return a mock instance of an AbstractValidSource subclass.

        This is helpful when you want to invoke SourceContentRetrievers without
        actually validating the source.

        """
        from logtweet.source.retrieve import AbstractValidSource
        class MockValidSource(AbstractValidSource):
            @staticmethod
            def is_valid(source_string: str) -> bool:
                return True
        return MockValidSource("this has no meaning")

    def test_return_content_from_mock_source_content_retriever(
        self,
        mock_valid_source: AbstractValidSource,
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
        mock_source_content_retriever = MockSourceContentRetriever(
            mock_valid_source,
        )

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
        mock_valid_source: AbstractValidSource,
    ) -> None:
        """An exception raised during content retrieval is not caught."""
        class TestExceptionError(Exception):
            pass

        from logtweet.source.retrieve import AbstractSourceContentRetriever
        class MockSourceContentRetriever(AbstractSourceContentRetriever):
            def get_content(self) -> str:
                raise TestExceptionError
        mock_source_content_retriever = MockSourceContentRetriever(
            mock_valid_source,
        )
        from logtweet.source.retrieve import get_log_content_from_source

        with pytest.raises(TestExceptionError):
            get_log_content_from_source(
                mock_source_content_retriever,
            )


# TEST: Create functional/integration test for the retrieval use case.
