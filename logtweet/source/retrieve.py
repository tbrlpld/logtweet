# -*- coding: utf-8 -*-

"""Retrieve log content from different sources."""

# TODO: Allow source to be local file. Handle the two possible types.


import abc

# from logtweet._source.online import OnlineLogSource  # noqa: WPS436



# TODO: Define an abstract Source base class. This will define the needed
#       functionality from the perspective of this module. The implementations
#       can then inherit from that abstract class and only need to implement
#       the desired functionality. I need to think about how to **restructure
#       the modules** to do that though. I need to avoid circular dependencies.

class AbstractValidSource(abc.ABC):
    """Abstract valid source class."""

    def __init__(self) -> None:
        """Initialize AbstractValidSource."""

    @staticmethod
    @abc.abstractmethod
    def is_valid() -> bool:
        """Source string is a valid source."""


class SourceContentRetrievalError(Exception):
    """
    Raise if error during content retrieval.

    This class is meant to be extended to more meaningful error types.

    """


class AbstractSourceContentRetriever(abc.ABC):
    """
    Abstract source content retriever class.

    This abstract class defines the required methods that subclasses should
    define.

    The initialization of this class requires an instance of a
    `AbstractValidSource` to be passed. This means the caller needs to create
    a valid source instance before the retriever can be initialized.

    """

    def __init__(self, valid_source: AbstractValidSource) -> None:
        """
        Initialize AbstractSourceContentRetriever.

        Parameters
        ----------
        valid_source: AbstractValidSource
            `AbstractValidSource` instance. If this is missing, the
            `SourceContentRetriever` can not be initialized.

        Raises
        ------
        TypeError
            If the `valid_source` is not an instance of a subclass of
            `AbstractValidSource`.

        """
        if not isinstance(valid_source, AbstractValidSource):
            raise TypeError(
                "Expected {0}".format(AbstractValidSource)
                + " got {0}".format(type(valid_source)),
            )
        self.valid_source = valid_source

    @abc.abstractmethod
    def get_content(self) -> str:
        """
        Return content string from the source.

        # noqa: DAR402

        Raises
        ------
        SourceContentRetrievalError
            This exception or any of its child exceptions may be raised if
            something went wrong during the content retrieval.

        """


def get_log_content_from_source(
    source_content_retriever: AbstractSourceContentRetriever,
) -> str:
    """
    Get log content from a source with the given source content retriever.

    Parameters
    ----------
    source_content_retriever: AbstractSourceContentRetriever
        Instance of an implemented of an AbstractSourceContentRetriever that
        handles the actual retrieving of the content when it's `get_content`
        method is called.

    Returns
    -------
    str
        Log content returned by the `SourceContentRetriever.get_content()`
        method.

    # noqa: DAR402

    Raises
    ------
    TypeError
        If passed `source_content_retriever` is not of correct type
        `AbstractSourceContentRetriever`.
    SourceContentRetrievalError
        This exception or any of its child exceptions may be raised if
        something went wrong during the content retrieval.

    """
    is_expected_type = isinstance(
        source_content_retriever,
        AbstractSourceContentRetriever,
    )
    if not is_expected_type:
        raise TypeError(
            "Expected {0}".format(AbstractSourceContentRetriever)
            + " got {0}".format(type(source_content_retriever)),
        )
    return source_content_retriever.get_content()
