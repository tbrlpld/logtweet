# -*- coding: utf-8 -*-

"""Module for main app functionality of logtweet."""

import argparse
from datetime import date, timedelta

from logtweet import conf, history, send, content
from logtweet.source.controllers import retrieve as ctrlretrieve


def main():
    """
    Create a tweet based on today's log message.

    Raises
    ------
    RuntimeError
        When function is run in a way that leads to attempting to send a tweet
        that has been sent before.

    """
    parser = create_arg_parser()
    args = parser.parse_args()

    day_date = date.today() + timedelta(days=args.offset)

    config = conf.get_config()
    source_string = config["LogTweet"]["source"]
    bitly_api_key = config.get(
        section="Bitly",
        option="api_key",
        fallback=None,
    )

    log_content = ctrlretrieve.get_log_content_from_source(source_string)

    tweet_content = content.get_tweet_content(
        log_content,
        day_date,
        bitly_api_key,
    )

    if args.testmode:
        print(tweet_content)
    else:
        # Check history before sending tweet to prevent duplication.
        tweeted_before = history.is_tweet_in_history(tweet_content)
        if tweeted_before:
            raise RuntimeError("Tweet with this content already exists!")
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
        default=0,
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
