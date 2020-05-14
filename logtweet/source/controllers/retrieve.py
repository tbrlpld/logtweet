# -*- coding: utf-8 -*-

"""
Controller for the log content retrieval.

This is the entry point to the retrieve usecase.

"""

from logtweet.source.usecases import retrieve as ucretrieve
from logtweet.source.adapters import onlineretriever as adaptonline
from logtweet.source.adapters import validurl as adapturl


def get_log_content_from_source(source_string: str) -> str:
    """
    Return log content from the source identified by the source string.

    Parameters
    ----------
    source_string : str
        String defining the source from which to retrieve the content.
        Currently, the source string has to be a valid url. But, this will
        be extended to allow local file paths in the future.

    Returns
    -------
    str
        Content string retrieved from the source.

    """
    # TODO: Allow source to be local file. Handle the two possible types.
    #       To allow the two source types, detect source type, then create the
    #       appropriate retriever object and call the use case with the
    #       created retriever.
    validurl = adapturl.ValidSourceURL(source_string)
    retriever = adaptonline.OnlineSourceContentRetriever(validurl)
    return ucretrieve.get_log_content_from_source(retriever)
