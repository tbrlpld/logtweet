# -*- coding: utf-8 -*-

"""Retrieve log content from a source."""

import abc


class SourceValidationError(Exception):
    """
    Raise if source could not be validated.

    This is only a base exception, intended to be extended by more specific
    validation errors.

    """


class AbstractValidSource(abc.ABC):
    """Abstract valid source class."""

    def __init__(self, source_string: str) -> None:
        """Initialize AbstractValidSource."""
        if not isinstance(source_string, str):
            raise TypeError(
                "Expected str, got {0}".format(type(source_string)),
            )
        if not self.is_valid(source_string):
            raise SourceValidationError

    @staticmethod
    @abc.abstractmethod
    def is_valid(source_string: str) -> bool:
        """
        Source string is a valid source.

        # noqa: DAR202

        Parameters
        ----------
        source_string : str
            String that identifies the source to validate.

        Returns
        -------
        bool
            `True` is the source is valid, `False` if not.

        # noqa: DAR402

        Raises
        ------
        SourceValidationError
            This is a subclass of this exception shall be raised if the
            validation fails.

        """


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
