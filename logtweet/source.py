# -*- coding: utf-8 -*-

"""Retrieve log content from different sources."""


from logtweet._source.online import OnlineLogSource


def get_log_content_from_source(source_string: str) -> str:
    """
    Get log content from the given source.

    A valid source needs to be (for now) a URL that can be reached. Validation
    errors are raised if the source location can not be identified or reached.

    Arguments:
        source_string (str): String identifying a valid source to pull the
            log content from.

    """
    online_obj = OnlineLogSource(source_string)
    return online_obj.content
