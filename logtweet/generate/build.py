# -*- coding: utf-8 -*-

"""Functions related to building the tweet content."""

import re


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
    # TODO: Allow days being marked as `Off-Day` in the heading.
    try:
        day = extract_day_number_from_heading_string(heading_string)
    except ValueError:
        raise ValueError(
            "Could not build preamble."
            + " Check the formatting of the given heading_string.",
        )
    return f"{day}/#100DaysOfCode"


def extract_day_number_from_heading_string(heading_string: str) -> int:
    """
    Extract day number from heading string.

    >>> extract_day_number_from_heading_string(
    ...    "Day 1: October 16, 2019, Wednesday",
    ... )
    1

    Arguments:
        heading_string (str): Day's log header string from which the day can be
            extracted. Expected format is something like
            `Day 1: October 16, 2019, Wednesday`.

    Returns:
        int: Day number string that was extracted from the heading string.

    Raises:
        ValueError: is raised if no day number could be extracted due to
            formatting issues.

    """
    day_str = re.sub(
        r"(Day\s)(\d+)(:.*)",
        r"\2",
        heading_string,
    )
    try:
        day = int(day_str)
    except ValueError:
        raise ValueError(
            "Could not extract day number."
            + " Check the formatting of the given `heading_string`.",
        )
    return day
