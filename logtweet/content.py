# -*- coding: utf-8 -*-

"""Module to generate tweet content from a log."""

import datetime
from typing import Optional

import bs4  # type: ignore

from logtweet._content import extract, build, shortlink  # noqa: WPS436


MAX_TWEET_LEN = 240


def get_tweet_content(
    log_string: str,
    day_date: datetime.date,
    bitly_api_key: Optional[str] = None,
) -> str:
    """
    Get tweet content from a log string for a given date.

    Arguments:
        log_string (str): String representation of the log. The log string is
            expected to contain an HTML log. The HMTL log is expected to
            contain contain ``<h2>`` elements for the day headings and ``<h3>``
            elements for the day's subsections.
            # TODO: Force these expectation on the content through custom
            #       types. The generation of the custom type validates the
            #       structure
        day_date (datetime.date): Day for which the tweet is to be generated.
        bitly_api_key (Opeional[str]): While generating the tweet content, the
            first link from the "Link(s)" section is extracted and shortened.
            The user if an API key for the Bit.ly service is provided, that
            service is used. This argument defaults to ``None``, in which case
            `Shorten That URL_ is used.

    Returns:
        str: Tweet content for the given ``day_date`` extracted from the
        ``log_string``.

    .. _`Shorten That URL: https://s.lpld.io

    """
    soup = bs4.BeautifulSoup(log_string, "html.parser")

    day_heading = extract.get_day_heading(soup, heading_date=day_date)

    # Generate tweet preamble (E.g. 77/#100DaysOfCode)
    preamble = build.make_preamble(day_heading.text)

    # Extract first link from list of links for the day.
    try:
        link = extract.get_first_link(day_heading)
    except LookupError:
        pass
    else:
        # Create shortened link to first link of the day.
        link = shortlink.get_short_link(link, bitly_api_key)

    # Calculate max message length. This needs to be the maximum tweet
    # length, reduced by the preamble and the link.
    # TODO: Create separate function to build tweet. The tweet template only
    #       needs to be available in that function.
    tweet_content_template = "{preamble} {tweet_message}\n\n{link}"
    tweet_length_wo_message = len(tweet_content_template.format(
        preamble=preamble,
        tweet_message="",
        link=link,
    ))
    max_length = MAX_TWEET_LEN - tweet_length_wo_message
    # Get content
    tweet_message = extract.get_tweet_message(day_heading, max_len=max_length)

    # Build content from preamble, message and link
    return tweet_content_template.format(
        preamble=preamble,
        tweet_message=tweet_message,
        link=link,
    )
