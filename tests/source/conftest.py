from typing import Callable, TYPE_CHECKING

import pytest  # type: ignore

if TYPE_CHECKING:
    from logtweet.source.adapters import onlineretriever as adaptonline


@pytest.fixture  # type: ignore
def valid_online_source_factory(
) -> Callable[[str], "adaptonline.AbstractValidOnlineSource"]:
    """
    Create factory function to create `adaptonline.AbstractValidOnlineSource` instance.

    Returns
    -------
    Callable[[str], "adaptonline.AbstractValidOnlineSource"]
        Factory function to create instances of a subclass of
        `adaptonline.AbstractValidOnlineSource`.

    """
    from logtweet.source.adapters import onlineretriever as adaptonline

    def valid_online_source(source_string: str) -> adaptonline.AbstractValidOnlineSource:
        """
        Create instance of `adaptonline.AbstractValidOnlineSource` subclass.

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
            instance of the `adaptonline.AbstractValidOnlineSource` subclass.

        Returns
        -------
        adaptonline.AbstractValidOnlineSource
            Instance of an internal subclass of `adaptonline.AbstractValidOnlineSource`.
            The object will have the given `source_string` available as its
            `url` property.

        """

        class ValidOnlineSourceForTest(adaptonline.AbstractValidOnlineSource):
            @staticmethod
            def is_valid(_: str) -> bool:
                return True

        return ValidOnlineSourceForTest(source_string)

    return valid_online_source
