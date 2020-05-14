# -*- coding: utf-8 -*-

"""Tests for the OnlineSourceRetriever class."""

from typing import Any, Callable, TYPE_CHECKING

import pytest  # type: ignore

if TYPE_CHECKING:
    from logtweet.source.online import AbstractValidOnlineSource
    import requests


class TestAbstractValidOnlineSourceClass(object):
    """Tests for `AbstractValidOnlineSource` class."""

    def test_subclass(self) -> None:
        """Is subclass of `AbstractValidSource`."""
        from logtweet.source.usecases.retrieve import AbstractValidSource
        from logtweet.source.online import AbstractValidOnlineSource

        assert issubclass(
            AbstractValidOnlineSource,
            AbstractValidSource,
        )

    def test_no_direct_instantiation(self) -> None:
        """Can not be instantiated directly, because is abstract."""
        from logtweet.source.online import AbstractValidOnlineSource

        with pytest.raises(
            TypeError,
            match=r"Can't instantiate.*abstract.*",
        ):
            AbstractValidOnlineSource()  # type: ignore

    def test_init_when_is_valid_defined(self) -> None:
        """Subclass init works if `is_valid` is defined."""
        from logtweet.source.online import AbstractValidOnlineSource
        class ValidTestOnlineSource(AbstractValidOnlineSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True

        ValidTestOnlineSource("not important")

    def test_url_property_available_on_instance(self) -> None:
        """
        A subclass instance has the `url` property.

        The `url` property should contain the string passed to the constructor.

        """
        from logtweet.source.online import AbstractValidOnlineSource
        class ValidTestOnlineSource(AbstractValidOnlineSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True
        string_to_validate = "Some string"

        valid_test_online_source = ValidTestOnlineSource(string_to_validate)

        assert valid_test_online_source.url == string_to_validate


class TestOnlineSourceRetrieverClass(object):
    """Tests for the ``OnlineSourceRetriever`` class."""

    def test_subclass(self) -> None:
        """OnlineSourceRetriever is subclass of AbstractSourceRetriever."""
        from logtweet.source.usecases.retrieve import AbstractSourceContentRetriever
        from logtweet.source.online import OnlineSourceContentRetriever

        assert issubclass(
            OnlineSourceContentRetriever,
            AbstractSourceContentRetriever,
        )


class TestOnlineSourceRetrieverInit(object):
    """Test the `init` method of the `OnlineSourceContentRetriever`."""


    def test_type_error_if_init_input_wrong_type(self) -> None:
        """Raise TypeError if init input parameter not right type."""
        class NotTheRightType(object):
            pass
        wrong_type_input = NotTheRightType()
        from logtweet.source.online import OnlineSourceContentRetriever

        with pytest.raises(
            TypeError,
            match=r"Expected .*, got .*",
        ):
            OnlineSourceContentRetriever(wrong_type_input)  # type: ignore

    def test_type_error_if_input_not_specific_enough(self) -> None:
        """
        Type error if input not specific enough.

        If the input is subclass of `AbstractValidSource` but not of
        `AbstractValidOnlineSource` the type error is also thrown.

        """
        from logtweet.source.usecases.retrieve import AbstractValidSource
        class NotSpecificEnoughSource(AbstractValidSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True
        not_specific_enough_source = NotSpecificEnoughSource("stuff")
        from logtweet.source.online import OnlineSourceContentRetriever

        with pytest.raises(
            TypeError,
            match=r"Expected .*, got .*",
        ):
            OnlineSourceContentRetriever(
                not_specific_enough_source,  # type: ignore
            )

    def test_init_success(
        self,
        valid_online_source_factory: Callable[[str], "AbstractValidOnlineSource"],
    ) -> None:
        """
        Successful init without error.

        Passing an instance of a `AbstractValidOnlineSource` subclass leads
        to successful init of `OnlineSourceContentRetriever`.

        """
        valid_online_source = valid_online_source_factory("not important")
        from logtweet.source.online import OnlineSourceContentRetriever

        OnlineSourceContentRetriever(valid_online_source)

    def test_valid_source_avaliable_on_instance(
        self,
        valid_online_source_factory: Callable[[str], "AbstractValidOnlineSource"],
    ) -> None:
        """Passed valid source object is available on the instance."""
        valid_online_source = valid_online_source_factory("not important")
        from logtweet.source.online import OnlineSourceContentRetriever

        instance = OnlineSourceContentRetriever(valid_online_source)

        assert instance.valid_source == valid_online_source

    def test_valid_source_has_url_property(
        self,
        valid_online_source_factory: Callable[[str], "AbstractValidOnlineSource"],
    ) -> None:
        """Valid source on instance has `url` property."""
        source_string = "not important"
        valid_online_source = valid_online_source_factory(source_string)
        from logtweet.source.online import OnlineSourceContentRetriever
        instance = OnlineSourceContentRetriever(valid_online_source)

        url = instance.valid_source.url

        assert url == source_string


class TestOnlineSourceRetrieverGetContentWhiteBox(object):
    """
    Tests for the `get_content` method of the `OnlineSourceRetriever`.

    These are white box tests, that heavily rely on mocking out the used
    `requests` library and specifically its `get` method. When the
    implementation changes, then these tests have to be changed.

    """

    status_codes = {
        "success": 200,
        "not_found": 404,
    }

    @staticmethod
    def mock_get_factory(
        status_code: int,
        page_content: str = "",
    ) -> Callable[[Any], "requests.Response"]:
        """
        Return a mock function to replace `requests.get()`.

        The mock get function will return a `requests.Response` object with
        the given `status_code` and `page_content`. The `page_content` string
        will be available as `Response.text`.

        Parameters
        ----------
        status_code : int
            Status code of the response object that the mock get function
            returns.
        page_content : str
            Page content that is available as the `text` property on the
            response object that the mock function returns.

        Returns
        -------
        Callable[[Any], requests.Response]
            Mock function to replace `requests.get`. Takes any arguments and
            ignores them. It returns a `requests.Response` object with the
            given `status_code` and `page_content`.

        """
        import requests

        def mock_get(*_args: Any, **_kwargs: Any) -> requests.Response:
            """
            Mock get function.

            Use this function to mock out `requests.get`. It returns a
            `requests.Response` object, just like the real function.

            All parameters passed to this function are ignored.

            Parameters
            ----------
            _args : Any
                All  positional parameters passed to this function are ignored.
            _kwargs : Any
                All keyword parameters passed to this function are ignored.

            Returns
            -------
            requests.Response
                Response object with `status_code` and `text`.

            """
            mock_resp = requests.Response()
            mock_resp.status_code = status_code
            mock_resp._content = bytes(page_content, encoding="utf-8")  # type: ignore

            return mock_resp

        return mock_get

    if TYPE_CHECKING:
        from logtweet.source.online import OnlineSourceContentRetriever

    @pytest.fixture  # type: ignore
    def online_source_content_retriever(
        self,
        valid_online_source_factory: Callable[[str], "AbstractValidOnlineSource"],
    ) -> "OnlineSourceContentRetriever":
        """
        Create an `OnlineSourceContentRetriever` object.

        This is a convenience fixture to instantiate an
        `OnlineSourceContentRetriever` object from a meaningless valid online
        source. The source is not actually validated.

        Parameters
        ----------
        valid_online_source_factory : Callable[[str], "AbstractValidOnlineSource"]
            Factory function fixture to create a valid online source instance
            from a given source string.

        Returns
        -------
        OnlineSourceContentRetriever
            The `OnlineSourceContentRetriever` object is instantiated with a
            valid online source, that is created with the
            `valid_online_source_factory`. The valid source is created with a
            meaningless string passed to it.

        """
        from logtweet.source.online import OnlineSourceContentRetriever

        valid_online_source = valid_online_source_factory("not important")
        online_source_content_retirever = OnlineSourceContentRetriever(
            valid_online_source,
        )

        return online_source_content_retirever

    def test_returns_page_content_from_mocked_requests_response_object(
        self,
        monkeypatch: Any,
        online_source_content_retriever: "OnlineSourceContentRetriever",
    ) -> None:
        """Return the content from mocked response object."""
        defined_content = "Some content"
        mock_get = self.mock_get_factory(
            self.status_codes["success"],
            defined_content,
        )
        from logtweet.source.online import requests  # type: ignore
        monkeypatch.setattr(
            requests,
            "get",
            mock_get,
        )

        actual_content = online_source_content_retriever.get_content()

        assert actual_content == defined_content

    def test_raises_error_for_requests_connection_error(
        self,
        monkeypatch: Any,
        online_source_content_retriever: "OnlineSourceContentRetriever",
    ) -> None:
        """Raises SourceContentRetrievalError when connection error. """
        from logtweet.source.online import requests  # type: ignore
        # Create mock function for `requests.get`
        def mock_get_raises_connection_error(*args: Any, **kwargs: Any) -> None:
            raise requests.ConnectionError
        # Activate the mock for `requests.get`
        monkeypatch.setattr(
            requests,
            "get",
            mock_get_raises_connection_error,
        )
        from logtweet.source.usecases.retrieve import SourceContentRetrievalError

        with pytest.raises(SourceContentRetrievalError):
            online_source_content_retriever.get_content()

    def test_raised_error_for_requests_connection_error_shows_url(
        self,
        monkeypatch: Any,
        online_source_content_retriever: "OnlineSourceContentRetriever",
    ) -> None:
        """Raises SourceContentRetrievalError when connection error. """
        from logtweet.source.online import requests  # type: ignore
        # Create mock function for `requests.get`
        def mock_get_raises_connection_error(*args: Any, **kwargs: Any) -> None:
            raise requests.ConnectionError
        # Activate the mock for `requests.get`
        monkeypatch.setattr(
            requests,
            "get",
            mock_get_raises_connection_error,
        )
        from logtweet.source.usecases.retrieve import SourceContentRetrievalError

        with pytest.raises(
            SourceContentRetrievalError,
            match=r".*{0}.*".format(online_source_content_retriever.valid_source.url)
        ):
            online_source_content_retriever.get_content()

    def test_raises_error_for_bad_status_code(
        self,
        monkeypatch: Any,
        online_source_content_retriever: "OnlineSourceContentRetriever",
    ) -> None:
        """Raise `SourceContentRetrievalError` when bad HTTP status code."""
        defined_content = "Some content"
        mock_get = self.mock_get_factory(
            self.status_codes["not_found"],
            defined_content,
        )
        from logtweet.source.online import requests  # type: ignore
        monkeypatch.setattr(
            requests,
            "get",
            mock_get,
        )
        from logtweet.source.usecases.retrieve import SourceContentRetrievalError


        with pytest.raises(SourceContentRetrievalError):
            online_source_content_retriever.get_content()

    def test_raised_error_for_bad_status_code_shows_code(
        self,
        monkeypatch: Any,
        online_source_content_retriever: "OnlineSourceContentRetriever",
    ) -> None:
        """Raise `SourceContentRetrievalError` when bad HTTP status code."""
        defined_content = "Some content"
        mock_get = self.mock_get_factory(
            self.status_codes["not_found"],
            defined_content,
        )
        from logtweet.source.online import requests  # type: ignore
        monkeypatch.setattr(
            requests,
            "get",
            mock_get,
        )
        from logtweet.source.usecases.retrieve import SourceContentRetrievalError

        with pytest.raises(
            SourceContentRetrievalError,
            match=r".*404.*",
        ):
            online_source_content_retriever.get_content()
