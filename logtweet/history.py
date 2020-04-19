# -*- coding: utf-8 -*-

"""Functions related to keeping a history of sent tweets."""

import datetime
import os

LOG_FILE = os.path.expanduser("~/.config/logtweet/tweet.log")


def add_tweet_to_history(
    tweet_content: str,
    history_filepath: str = LOG_FILE,
) -> None:
    """
    Add tweet to history file.

    Arguments:
        tweet_content (str): Tweet content string for which an entry shall be
            created in the history file. The tweet is converted into a single
            line by calling the ``create_tweet_history_msg()`` on it.
        history_filepath (str): Optional path string to the history file to
            append the tweet to. Default is ``logtweet.LOG_FILE``.

    """
    tweet_history_msg = create_tweet_history_msg(tweet_content)
    full_line = "{0} - Sent : {1}\n".format(
        datetime.datetime.now(),
        tweet_history_msg,
    )
    with open(history_filepath, "a") as history_file:
        history_file.writelines(full_line)


def is_tweet_in_history(
    tweet_content: str,
    history_filepath: str = LOG_FILE,
) -> bool:
    """
    Check if the history contains a message representing the tweet_content.

    Arguments:
        tweet_content (str): Tweet content string.
        history_filepath (str): Path string to the history file that is to be
            checked for the tweet content representation.

    Returns:
        bool: Expresses if the tweet was sent before (and therefore is in the
            history).

    """
    tweet_logging_msg = create_tweet_history_msg(tweet_content)
    return is_string_in_filelines(tweet_logging_msg, filepath=history_filepath)


def create_tweet_history_msg(tweet_content: str) -> str:
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
