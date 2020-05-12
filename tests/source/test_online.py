# -*- coding: utf-8 -*-

"""Tests for the OnlineSourceRetriever class."""

import pytest  # type: ignore


# TEST: Mock actually available online server. So run an HTTP server for the
#       test. Python comes with the simple `http.server` module that allows
#       just that.

class TestAbstractValidOnlineSource(object):
    """Tests for `AbstractValidOnlineSource` class."""

    def test_subclass(self) -> None:
        """Is subclass of `AbstractValidSource`."""
        from logtweet.source.retrieve import AbstractValidSource
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
        from logtweet.source.retrieve import AbstractSourceContentRetriever
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
        from logtweet.source.retrieve import AbstractValidSource
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

    from logtweet.source.online import AbstractValidOnlineSource
    @pytest.fixture  # type: ignore
    def valid_test_online_source(self) -> AbstractValidOnlineSource:
        from logtweet.source.online import AbstractValidOnlineSource
        class ValidTestOnlineSource(AbstractValidOnlineSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True
        return ValidTestOnlineSource("not important")

    def test_init_success(
        self,
        valid_test_online_source: AbstractValidOnlineSource,
    ) -> None:
        """
        Successful init without error.

        Passing an instance of a `AbstractValidOnlineSource` subclass leads
        to successful init of `OnlineSourceContentRetriever`.

        """
        from logtweet.source.online import OnlineSourceContentRetriever

        OnlineSourceContentRetriever(valid_test_online_source)

    def test_valid_source_avaliable_on_instance(
        self,
        valid_test_online_source: AbstractValidOnlineSource,
    ) -> None:
        """Passed valid source object is available on the instance."""
        from logtweet.source.online import OnlineSourceContentRetriever

        instance = OnlineSourceContentRetriever(valid_test_online_source)

        assert instance.valid_source == valid_test_online_source

    def test_valid_source_has_url_property(
        self,
        valid_test_online_source: AbstractValidOnlineSource,
    ) -> None:
        """Valid source on instance has `url` property."""
        from logtweet.source.online import OnlineSourceContentRetriever
        instance = OnlineSourceContentRetriever(valid_test_online_source)

        url = instance.valid_source.url

        assert url == "not important"


# class TestGetContentFromOnlineSource(object):
#     """Test `get_content_from_online_source` static method."""

#     @staticmethod
#     def mock_get_factory(status_code: int, page_content: str = ""):
#         import requests
#         def mock_get(*args, **kwargs):
#             mock_resp = requests.Response()
#             mock_resp.status_code = status_code
#             mock_resp._content = bytes(page_content, encoding="utf-8")
#             return mock_resp
#         return mock_get

#     def test_returns_page_content_from_passed_source_string(
#         self,
#         monkeypatch,
#         valid_url_obj,
#     ):
#         mock_page_content = "<html><body>The content</body></html>"
#         from logtweet._source.online import requests
#         monkeypatch.setattr(
#             requests,
#             "get",
#             self.mock_get_factory(200, mock_page_content),
#         )
#         from logtweet._source.online import get_content_from_url

#         returned_page_content = get_content_from_url(
#             valid_url_obj,
#         )

#         assert returned_page_content == mock_page_content

#     def test_raises_error_for_404(
#         self,
#         monkeypatch,
#         valid_url_obj,
#     ):
#         mock_page_content = "<html><body>The content</body></html>"
#         from logtweet._source.online import requests
#         monkeypatch.setattr(
#             requests,
#             "get",
#             self.mock_get_factory(404, mock_page_content),
#         )
#         from logtweet._source.exceptions import HTTPStatusError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(HTTPStatusError):
#             get_content_from_url(valid_url_obj)

#     def test_error_for_404_shows_status_code(
#         self,
#         monkeypatch,
#         valid_url_obj,
#     ):
#         mock_page_content = "<html><body>The content</body></html>"
#         from logtweet._source.online import requests
#         monkeypatch.setattr(
#             requests,
#             "get",
#             self.mock_get_factory(404, mock_page_content),
#         )
#         from logtweet._source.exceptions import HTTPStatusError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(HTTPStatusError, match=r".*404.*"):
#             get_content_from_url(valid_url_obj)

#     def test_raises_error_for_connection_error(self, monkeypatch, valid_url_obj):
#         from logtweet._source.online import requests
#         def mock_get_raises_connection_error(*args, **kwargs):
#             raise requests.ConnectionError
#         monkeypatch.setattr(
#             requests,
#             "get",
#             mock_get_raises_connection_error,
#         )
#         from logtweet._source.exceptions import RequestError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(RequestError):
#             get_content_from_url(valid_url_obj)

#     def test_raised_error_for_connection_error_shows_url(
#         self,
#         monkeypatch,
#         valid_url,
#         valid_url_obj,
#     ):
#         from logtweet._source.online import requests
#         def mock_get_raises_connection_error(*args, **kwargs):
#             raise requests.ConnectionError
#         monkeypatch.setattr(
#             requests,
#             "get",
#             mock_get_raises_connection_error,
#         )
#         from logtweet._source.exceptions import RequestError
#         from logtweet._source.online import get_content_from_url

#         with pytest.raises(
#             RequestError,
#             match=r".*{0}.*".format(valid_url),
#         ):
#             get_content_from_url(valid_url_obj)

#     def test_raises_type_error_if_input_not_valid_url_instance(
#         self,
#         valid_url,
#     ):
#         """
#         Test raises type error if input is not instance of  ``ValidUrl``.

#         E.g. if the input is of type string (even if this represents a valid
#         URL) the type error is raised. The caller is expected to validate the
#         URL by creating a corresponding object.

#         """
#         from logtweet._source.online import get_content_from_url
#         assert isinstance(valid_url, str)

#         with pytest.raises(TypeError):
#             get_content_from_url(valid_url)

