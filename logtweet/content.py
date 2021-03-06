# -*- coding: utf-8 -*-

"""Module to generate tweet content from a log."""

import datetime
from typing import Optional

import bs4  # type: ignore

from logtweet._content import extract, build, shortlink  # noqa: WPS436


def get_tweet_content(
    log_string: str,
    day_date: datetime.date,
    bitly_api_key: Optional[str] = None,
) -> str:
    """
    Get tweet content from a log string for a given date.

    Parameters
    ----------
    log_string : str
        String representation of the log. The log string is expected to contain
        an HTML log. The HMTL log is expected to contain contain ``<h2>``
        elements for the day headings and ``<h3>`` elements for the day's
        subsections.
        # TODO: Force these expectation on the content through custom
        #       types. The generation of the custom type validates the
        #       structure
    day_date : datetime.date
        Day for which the tweet is to be generated.
    bitly_api_key : Optional[str]
        While generating the tweet content, the first link from the "Link(s)"
        section is extracted and shortened.
        The user if an API key for the Bit.ly service is provided, that
        service is used. This argument defaults to ``None``, in which case
        `Shorten That URL_ is used.

    Returns
    -------
    str
        Tweet content for the given `day_date` extracted from the `log_string`.

    .. _`Shorten That URL: https://s.lpld.io

    """
    soup = bs4.BeautifulSoup(log_string, "html.parser")

    day_heading = extract.get_day_heading(soup, heading_date=day_date)
    day_number = extract.get_day_number_from_heading_string(day_heading.text)
    try:
        link = extract.get_first_link(day_heading)
    except LookupError:
        link = ""
    else:
        link = shortlink.get_short_link(link, bitly_api_key)

    # Generate tweet preamble (E.g. 77/#100DaysOfCode)
    preamble = build.make_preamble(day_number)
    # Calculate max message length. This needs to be the maximum tweet
    # length, reduced by the preamble and the link.
    max_tweet_msg_len = calc_max_tweet_msg_len(preamble, link)
    # Get content
    progress_paragraphs = extract.get_progress_paragraphs(day_heading)
    tweet_message = build.join_strings_to_max_len(
        strings=progress_paragraphs,
        max_len=max_tweet_msg_len,
        sep="\n\n",
    )

    # Build content from preamble, message and link
    return build.make_tweet_content(
        preamble=preamble,
        message=tweet_message,
        link=link,
    )


def calc_max_tweet_msg_len(
    preamble: str,
    link: str,
    max_tweet_len: int = 240,
) -> int:
    """
    Calculate maximum tweet message length.

    The available length for the message is simply the subtraction of the
    preamble, the link and the white spaces in an empty tweet from the maximum
    tweet length.

    Parameters
    ----------
    preamble :str
        Preamble to be used in the beginning of the tweet.
    link : str
        Link to be added in the end of the tweet.
    max_tweet_len : int
        Optional. Maximum tweet length. Default is 240.

    Returns
    -------
    int
        Length available for the tweet message, when combined with the given
        preamble and link.

    """
    tweet_length_wo_message = len(build.make_tweet_content(
        preamble=preamble,
        message="",
        link=link,
    ))
    return max_tweet_len - tweet_length_wo_message
