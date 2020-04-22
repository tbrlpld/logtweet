# -*- coding: utf-8 -*-

"""Functions related to building the tweet content."""


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
