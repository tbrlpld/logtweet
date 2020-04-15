# -*- coding: utf-8 -*-

"""Module to post tweet based on today's #100DaysOfCode log."""

# TODO: Refactor this into multiple modules. This is way to long right now.

import argparse
from datetime import date, datetime, timedelta
import logging
import os
import re
from typing import Optional

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore
import requests
import tweepy  # type: ignore

from logtweet.conf import get_config


config = get_config()

URL = config["LogTweet"]["url"]
DATE_FORMAT = "%B %d, %Y"  # noqa: WPS323
MAX_TWEET_LEN = 240
LOG_FORMAT = "%(asctime)s %(name)-10.10s %(levelname)-4.4s %(message)s"  # noqa: WPS323, E501
LOG_FILE = os.path.expanduser("~/.config/logtweet/tweet.log")

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    filename=LOG_FILE,
    filemode="a",  # append
)


def main():
    """Create a tweet based on today's log message."""
    parser = create_arg_parser()
    args = parser.parse_args()
    offset = args.offset

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get today's heading
    today_date = date.today() + timedelta(days=offset)
    today_heading = get_day_heading(soup, heading_date=today_date)

    # Generate tweet preamble (E.g. 77/#100DaysOfCode)
    preamble = build_preamble(today_heading.text)

    # Extract first link from list of links for the day.
    try:
        link = get_first_link(today_heading)
    except LookupError:
        pass
    else:
        # Create shortened link to first link of the day.
        bitly_api_key = config.get(
            section="Bitly",
            option="api_key",
            fallback=None,
        )
        link = get_short_link(link, bitly_api_key)

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
    tweet_message = get_tweet_message(today_heading, max_len=max_length)

    # Build content from preamble, message and link
    tweet_content = tweet_content_template.format(
        preamble=preamble,
        tweet_message=tweet_message,
        link=link,
    )

    send_tweet(tweet_content, test_mode=args.testmode)


def create_arg_parser() -> argparse.ArgumentParser:
    """
    Create the created argument parser.

    Returns:
        argparse.ArgumentParser: Argument parser instance for this app.

    """
    parser = argparse.ArgumentParser(description="Tweet todays log message.")
    parser.add_argument(
        "-o",
        "--offset",
        type=int,
        help=(
            "Days to offset the today value with."
            + " Can be positive or negative."
        ),
    )
    parser.add_argument(
        "-t",
        "--testmode",
        action="store_true",
        help=(
            "Run in test mode. Everything is run the same, but the tweet is"
            + " only printed to stdout. No tweet is sent and no log message is"
            + " created."
        ),
    )
    return parser


def heading_matches_date(day_heading_text: str, given_date: date) -> bool:
    """
    Check if given day heading represents the given date.

    Arguments:
        day_heading_text (str) : String to extract the date from. Expected
            format like this: "Day 1: October 16, 2019, Wednesday".
        given_date (date): datetime.date object to check the heading
            text against.

    Returns:
        bool: Expresses if the given day heading text represents the given
            date.

    """
    # Extract the date string
    # TODO: Create separate function for the date_string extraction.
    # A separate function makes this easier to test.
    date_string = re.sub(
        r"(.*: )(.*)(, .*day.*)",  # pattern to create groups
        r"\2",  # Return only second group
        day_heading_text,
    )
    # Convert to date object
    date_obj = datetime.strptime(date_string, DATE_FORMAT).date()

    return date_obj == given_date


def get_day_heading(soup: BeautifulSoup, heading_date: date) -> Tag:
    """
    Return today's heading element or None.

    Arguments:
        soup (BeautifulSoup): Soup object of log page parsed with
            BeautifulSoup.
        heading_date (date): ``datetime.date`` object for which the heading
            shall be extracted.

    Returns:
        Tag: Heading element representing today.
        None: If no heading element for today was found.

    Raises:
        LookupError: Raised if no heading element for today was found.

    """
    day_headings = soup.find_all("h2")
    for day in day_headings[::]:
        if heading_matches_date(day.text, heading_date):
            return day
    raise LookupError("No heading found for today!")


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


def get_day_subheading_by_text(
    day_heading: Tag,
    subheading_text: str,
) -> Tag:
    """
    Retrieve the next subheader (h3) element with the given text.

    This function only iterates over the following sibling's of the given
    ``day_heading`` until the next day heading (h2) is found.

    Arguments:
        day_heading (Tag): Tag element of a day's header. This is the
            starting point to look for following sibling subheaders.
        subheading_text (str): Content string for the searched subheader, which
            can be retrieved from the subheader element with
            ``subheader.text``.

    Returns:
        Tag: Found subheader element with given ``.text`` attribute.

    Raises:
        LookupError: if no subheader with the given ``.text`` attribute could
            be found after the given ``day_heading`` element and before the
            next.

    """
    # Go over the next siblings until the next day heading is found
    current_element = day_heading
    while True:
        next_sibling = current_element.next_sibling
        if not next_sibling or next_sibling.name == "h2":
            break
        if next_sibling.name == "h3" and next_sibling.text == subheading_text:
            return next_sibling
        current_element = next_sibling
    raise LookupError(
        "No subheading with text '{0}' could be found".format(subheading_text)
        + " after the day heading '{0}'!".format(day_heading),
    )


def get_first_link(day_heading: Tag) -> Optional[str]:
    """
    Extract the first link  URL from the list of the day's links.

    Expects the following structure after the day header:

    ::

        <h2>Day 1: October 16, 2019, Wednesday</h2>
        ...
        <h3>Link(s)</h3>
        <ol>
          <li><a href="http://example.com/1">Example Link 1</a></li>
          <li><a href="http://example.com/2">Example Link 2</a></li>
        </ol>

    For the given example, it would return "http://example.com/1".

    Arguments:
        day_heading (Tag): Day's log header element which is followed by the
            subheadings. The ``Link(s)`` subheading in turn needs to be
            followed by an ordered list. The link address (``href``) found in
            the anchor element of the first list item is returned.

    Returns:
        str: First link address found in the first list item.

    Raises:
        LookupError: is raised if no link could be found under the day's
            heading. This also includes anchor element for empty ``href``
            attribute.

    """
    link_address = None
    link_heading = get_day_subheading_by_text(day_heading, "Link(s)")
    try:
        link_address = (
            link_heading.find_next_sibling(  # type: ignore
                "ol",
            ).li.a.get("href")
        )
    except AttributeError:
        pass
    if not link_address:  # Catches empty link addresses and None
        raise LookupError(
            "No link extracted."
            + " Please check that a link list exists under the day's heading.",
        )
    return link_address


def get_short_link(long_link: str, bitly_api_key: Optional[str] = None) -> str:
    """
    Create short link.

    If a Bitly API key is passed, then the Bitly service is used to generate
    the short link. Otherwise it defaults to the URL shortener at
    `https://s.lpld.io`.

    Arguments:
        long_link (str): Long link to shorten.
        bitly_api_key (Optional[str]): API key for the Bit.ly service.
            See the `Bitly API documentation`_ on how to retrieve an API key.
            Default is `None`.

    Returns:
        str: Shortened link pointing to the same resource as the long link.

    .. _Bitly API documentation:
        https://dev.bitly.com/v4/#section/Application-using-a-single-account

    """
    # TODO: Split into separate functions for default and Bit.ly shortener.
    shortener_url = "https://s.lpld.io/create"
    headers = {}
    shortlink_key = "short"
    if bitly_api_key:
        shortener_url = "https://api-ssl.bitly.com/v4/shorten"
        headers["Authorization"] = f"Bearer {bitly_api_key}"
        shortlink_key = "link"
    payload = {"long_url": long_link}
    response = requests.post(shortener_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()[shortlink_key]


def get_tweet_message(day_heading: Tag, max_len: int) -> str:
    """
    Extract the tweet content from the paragraphs after content heading.

    Arguments:
        day_heading (Tag): Heading tag element for today.
        max_len (int): Maximum length of tweet message.

    Returns:
        str: Tweet message with a maximum length of max_len

    Raises:
        LookupError: is raised if no content heading is found or the extracted
            message is empty.

    """
    # Grab today's content heading
    content_heading = get_day_subheading_by_text(
        day_heading,
        "Today's Progress",
    )
    # Loop over the next siblings until you find something
    # that is not a paragraph. Extract content from the paragraphs until
    # maximum tweet length is reached.
    current_element = content_heading
    tweet_message = ""
    while True:
        possible_content = tweet_message
        next_sibling = current_element.find_next_sibling()
        if not next_sibling or next_sibling.name != "p":
            # Leave loop if no more siblings (end of page) or not a paragraph.
            break
        current_element = next_sibling

        # TODO: Separate function to concatenate message content
        possible_content = "{existing_content}\n\n{new_content}".format(
            existing_content=possible_content,
            new_content=current_element.text,
        ).strip()

        if len(possible_content) > max_len:
            # When possible content is longer than maximum before any thing is
            # extracted, a special error is raised to allow explicit handling
            # of this issue. This can go unhandled so that the user becomes
            # aware of this issue and can adjust the content in the log.
            if not tweet_message:
                raise ValueError(
                    "The first paragraph is too long!"
                    + " Maximum length: {}".format(max_len)
                    + " Extracted content: '{}'".format(possible_content)
                )
            break
        tweet_message = possible_content

    if not tweet_message:
        raise LookupError("No message found that could be tweeted!")
    return tweet_message


def twitter_authenticate(
    api_key: str,
    api_secret: str,
    access_token: str,
    access_secret: str,
) -> tweepy.API:
    """
    Create authenticated Tweepy API.

    Requires twitter API access information.

    Arguments:
        api_key (str): Twitter API key
        api_secret (str): Twitter API secret
        access_token (str): Twitter API access token
        access_secret (str): Twitter API access secret

    Returns:
        tweepy.API: Authenticated tweepy API object.

    """
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)


def create_tweet_logging_msg(tweet_content: str) -> str:
    """
    Create logging message based on tweet content.

    Arguments:
        tweet_content (str): Content string of the tweet.

    Returns:
        str: Single line log message for the tweet. Log messages should be
            single line for readability and extraction. Therefore, newline
            characters are replaced with spaces.

    """
    return tweet_content.replace("\n", " ")


def is_string_in_filelines(search_string: str, filepath: str) -> bool:
    """
    Check if string can be found in file.

    File is checked line by line. Thus, strings spanning multiple lines are not
    supported.

    Arguments:
        search_string (str): String to lookup in the lines of the file.
        filepath (str): String path of the file to check.

    Returns:
        bool: Expresses if the ``search_string`` was found in the file.

    """
    with open(filepath, "r") as file_obj:
        return any(
            search_string in line for line in file_obj.readlines()
        )


def send_tweet(tweet_content: str, test_mode: bool = False) -> None:
    """
    Send tweet with given content.

    For this to work, the config needs to contain valid Twitter API key and
    access token.

    Arguments:
        tweet_content (str): Content of the tweet.
        test_mode (bool): If ``True``, prints the tweet only to stdout but does
            not really send it to the Twitter API. Default is ``False``.

    Raises:
        RuntimeError: Raised if the defined tweet content was posted before.

    """
    # Check log before sending tweet to prevent duplication.
    # TODO: Move check for existing tweet to separate function.
    tweet_logging_msg = create_tweet_logging_msg(tweet_content)
    tweeted = is_string_in_filelines(tweet_logging_msg, filepath=LOG_FILE)
    if tweeted:
        warn_msg = "Tweet with this content already exists!"
        logging.warning(warn_msg)
        raise RuntimeError(warn_msg)
    # TODO: Move authentication. Authentication only needed when not test mode.
    tweepy_api = twitter_authenticate(
        config["Twitter"]["api_key"],
        config["Twitter"]["api_secret"],
        config["Twitter"]["access_token"],
        config["Twitter"]["access_secret"],
    )
    # TODO: Flip this to handle the test case first.
    if test_mode is False:
        # Send tweet
        tweepy_api.update_status(tweet_content)
        # Log tweet
        logging.info(tweet_logging_msg)
        # TODO: Add success message to user.
    else:
        print(tweet_content)  # noqa: WPS421
