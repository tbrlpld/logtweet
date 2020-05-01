# -*- coding: utf-8 -*-

"""Functions related to building the tweet content."""

from typing import Sequence

from logtweet._content import exceptions


def make_preamble(day_number: int) -> str:
    """
    Build preamble for tweet.

    The preamble for e.g. day 77 would look like: "77/#100DaysOfCode".

    Arguments:
        day_number (int): Integer number of the day

    Returns:
        str: Preamble for the tweet message.

    Raises:
        TypeError: if input is not an integer.

    """
    if not isinstance(day_number, int):
        raise TypeError(
            "Expected 'int', got '{0}'".format(type(day_number).__name__),
        )
    return f"{day_number}/#100DaysOfCode"


def make_tweet_content(preamble: str, message: str, link: str) -> str:
    """
    Make formatted tweet message from preamble, message and link.

    Arguments:
        preamble (str): Preamble to be used in the beginning of the tweet.
        message (str): Main message of the tweet.
        link (str): Link to be added in the end of the tweet.

    Returns:
        str: Full tweet content. If only empty strings are passed, this string
            still contains the white space used to format the message.

    """
    return f"{preamble} {message}\n\n{link}"


def join_strings_to_max_len(strings: Sequence[str], max_len: int) -> str:
    """Join string to a maximum given amount."""

    if len(strings[0]) > max_len:
        raise exceptions.StringJoiningError(
            "First string longer than maximum length!"
            + " Maximum length: {0}".format(max_len)
            + ", First string: {0}".format(strings[0]),
        )
