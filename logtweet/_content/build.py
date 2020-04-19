# -*- coding: utf-8 -*-

"""Functions related to building the tweet content."""

# TODO: Rename all builder functions ``make_...``

from logtweet._content.extract import extract_day_number_from_heading_string


def build_preamble(heading_string: str) -> str:
    """
    Build preamble for tweet.

    The preamble for e.g. day 77 would look like: "77/#100DaysOfCode".

    Arguments:
        heading_string (str): Day's log header string from which the day can be
            extracted. Expected format is something like
            `Day 1: October 16, 2019, Wednesday`.

    Returns:
        str: Preamble for the tweet message.

    Raises:
        ValueError: if the preamble could not be build.

    """
    # TODO: Remove extraction dependency. Take needed values as input.
    #       Let caller gather needed input.
    try:
        day = extract_day_number_from_heading_string(heading_string)
    except ValueError:
        raise ValueError(
            "Could not build preamble."
            + " Check the formatting of the given heading_string.",
        )
    return f"{day}/#100DaysOfCode"


