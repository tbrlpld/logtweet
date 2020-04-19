# -*- coding: utf-8 -*-

"""Module for main app functionality of logtweet."""

import argparse
from datetime import date, timedelta

import requests

from logtweet import conf, history, send, content


def main():
    """Create a tweet based on today's log message."""
    parser = create_arg_parser()
    args = parser.parse_args()

    day_date = date.today() + timedelta(days=args.offset)

    config = conf.get_config()
    url = config["LogTweet"]["url"]
    bitly_api_key = config.get(
        section="Bitly",
        option="api_key",
        fallback=None,
    )

    # TODO: Add validation that this is actually a URL. This would go hand in
    #       hand with creating other options for sources. Validation should be
    #       placed in custom classes. The instantiation of the class fails if
    #       the source does not match the expected type. Chaining try-except
    #       blocks allows testing for multiple possible source types. When all
    #       possible sources fail, inform the user.
    response = requests.get(url)

    tweet_content = content.get_tweet_content(
        response.text,
        day_date,
        bitly_api_key,
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
