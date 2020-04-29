# -*- coding: utf-8 -*-

"""Retrieve log content from different sources."""


from logtweet._source.online import OnlineLogSource  # noqa: WPS436


def get_log_content_from_source(source_string: str) -> str:
    """
    Get log content from the given source.

    A valid source needs to be (for now) a URL that can be reached. Validation
    errors are raised if the source location can not be identified or reached.

    # TODO: Allow source to be local file. Handle the two possible types.

    Parameters
    ----------
    source_string : str
        String identifying a valid source to pull the log content from.

    Returns
    -------
    str
        Log content extracted from the source which is identified by the given
        source string.

    Raises
    ------
    NotAUrlError
        If the passed source string is not a valid URL.
    RequestError
        When the network connection to the URL target fails.
    HTTPStatusError
        When the URL host responds with an error status code.

    # noqa: DAR402

    """
    online_obj = OnlineLogSource(source_string)
    return online_obj.content

# TODO: Define an abstract Source base class. This will define the needed
#       functionality from the perspective of this module. The implementations
#       can then inherit from that abstract class and only need to implement
#       the desired functionality. I need to think about how to **restructure
#       the modules** to do that though. I need to avoid circular dependencies.
