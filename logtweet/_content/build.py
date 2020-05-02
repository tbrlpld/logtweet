# -*- coding: utf-8 -*-

"""Functions related to building the tweet content."""

from typing import Union, List, Tuple

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


def join_strings_to_max_len(
    strings: Union[List[str], Tuple[str]],
    max_len: int,
    sep: str = "",
) -> str:
    """
    Join strings to a maximum given amount.

    Parameters
    ----------
    strings: Union[List[str], Tuple[str]]
        List or tuple of strings that shall be joined.
    max_len: int
        Maximum length of the returned string.

    """

    if not strings:
        raise ValueError("Passed sequence is empty. Can not join strings.")

    if max_len < 0:
        raise ValueError(
            "Maximum length is negative."
            + " Only positive values are acceptable.",
        )

    if len(strings[0]) > max_len:
        raise exceptions.FirstStringLongerThanMaxError(strings, max_len)

    joined = ""
    for string in strings:
        if not joined:
            joined = string
        elif (len(joined) + len(string)) <= max_len:
            joined += sep + string

    return joined.strip()
