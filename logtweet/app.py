# -*- coding: utf-8 -*-

"""Module for main app functionality of logtweet."""

# TODO: Refactor this into multiple modules. This is way to long right now.
# TODO: Move business logic from init to separate file. Only use init file
#       to expose public functions.

import argparse
from datetime import date, timedelta

from bs4 import BeautifulSoup  # type: ignore
import requests

from logtweet import conf, history, send
from logtweet.generate import extract, build


config = conf.get_config()

URL = config["LogTweet"]["url"]
MAX_TWEET_LEN = 240


def main():
    """Create a tweet based on today's log message."""
    # TODO: Create tests for main function.
    parser = create_arg_parser()
    args = parser.parse_args()
    offset = args.offset

    # TODO: Move every thing that is related to generating the tweet content to
    #       a separate function. All that the app is doing on the highest
    #       level, which is what the main is concerned with, is generating a
    #       tweet message from some source for a given date and then send it
    #       (or print if in test mode). It also wants to prevent duplicate
    #       tweets -- which is a high level decision in the app design.
    #       All other details should be abstracted into lower functions.
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get today's heading
    today_date = date.today() + timedelta(days=offset)
    today_heading = extract.get_day_heading(soup, heading_date=today_date)

    # Generate tweet preamble (E.g. 77/#100DaysOfCode)
    preamble = build.build_preamble(today_heading.text)

    # Extract first link from list of links for the day.
    try:
        link = extract.get_first_link(today_heading)
    except LookupError:
        pass
    else:
        # Create shortened link to first link of the day.
        # TODO: Move the link API handling into the link function/module.
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
    tweet_message = extract.get_tweet_message(today_heading, max_len=max_length)

    # Build content from preamble, message and link
    tweet_content = tweet_content_template.format(
        preamble=preamble,
        tweet_message=tweet_message,
        link=link,
    )

    if args.testmode:
        print(tweet_content)
    else:
        # Check log before sending tweet to prevent duplication.
        tweeted_before = history.is_tweet_in_history(tweet_content)
        if tweeted_before:
            err_msg = "Tweet with this content already exists!"
            raise RuntimeError(err_msg)
        # Send the tweet
        send.send_tweet(tweet_content, config["Twitter"])
        # Create history record of sent tweet for future lookup.
        history.add_tweet_to_history(tweet_content)
        # TODO: Add success message to user.


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
