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

class AbstractSourceContentRetriever(abc.ABC):
    """
    Abstract source class.

    This abstract class defines the required methods that subclasses should
    define.
    """

    @abc.abstractproperty
    def get_content(self) -> str:
        """Return content string from the source."""
        pass


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

    Raises
    ------
    SourceContentRetrievalError
        This exception or any of its child exceptions may be raised if
        something went wrong during the content retrieval.

    # noqa: DAR402

    """
    return source_content_retriever.get_content()
