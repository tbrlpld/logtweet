from typing import Callable, TYPE_CHECKING

import pytest  # type: ignore

if TYPE_CHECKING:
    from logtweet.source.adapters.onlineretriever import AbstractValidOnlineSource


@pytest.fixture  # type: ignore
def valid_online_source_factory(
) -> Callable[[str], "AbstractValidOnlineSource"]:
    """
    Create factory function to create `AbstractValidOnlineSource` instance.

    Returns
    -------
    Callable[[str], "AbstractValidOnlineSource"]
        Factory function to create instances of a subclass of
        `AbstractValidOnlineSource`.

    """
    from logtweet.source.adapters.onlineretriever import AbstractValidOnlineSource

    def valid_online_source(source_string: str) -> AbstractValidOnlineSource:
        """
        Create instance of `AbstractValidOnlineSource` subclass.

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
            instance of the `AbstractValidOnlineSource` subclass.

        Returns
        -------
        AbstractValidOnlineSource
            Instance of an internal subclass of `AbstractValidOnlineSource`.
            The object will have the given `source_string` available as its
            `url` property.

        """

        class ValidOnlineSourceForTest(AbstractValidOnlineSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True

        return ValidOnlineSourceForTest(source_string)

    return valid_online_source
