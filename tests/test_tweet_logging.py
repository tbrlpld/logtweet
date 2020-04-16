# -*- coding: utf-8 -*-
# TODO: Rename this and the actual module from "tweet_logging" to "history".
#       The fact that I am using the logging module is an implementation
#       detail. This should be hidden. Also "tweet_logging" is a little
#       confusing because the tweet is generated from a "log".

import pytest  # type: ignore


class TestCreateTweetLoggingMsg(object):
    """Tests for ``create_tweet_logging_msg`` function."""

    def test_turn_multiline_tweet_into_single_line_logging_msg(self):
        tweet_content = "This is a\n\nmultiline\n\ntweet."
        expected_msg = "This is a  multiline  tweet."
        from logtweet import create_tweet_logging_msg

        actual_msg = create_tweet_logging_msg(tweet_content)

        assert actual_msg == expected_msg


class TestIsStringInFile(object):
    """Tests for ``is_string_in_filelines`` function."""

    def test_finds_string_alone_in_line(self, test_file):
        search_string = "This is what I am looking for."
        file_content = f"""This is some thing.
{search_string}
This is something else."""
        test_file.write_text(file_content)
        from logtweet import is_string_in_filelines

        found = is_string_in_filelines(
            search_string,
            filepath=test_file.as_posix(),
        )

        assert found is True

    def test_finds_string_with_prefix_in_line(self, test_file):
        search_string = "This is what I am looking for."
        file_content = f"""This is some thing.
Here is something, but '{search_string}' is in this line too.
This is something else."""
        test_file.write_text(file_content)
        from logtweet import is_string_in_filelines

        found = is_string_in_filelines(
            search_string,
            filepath=test_file.as_posix(),
        )

        assert found is True

    def test_false_for_string_not_in_file(self, test_file):
        search_string = "This is what I am looking for."
        file_content = f"""This is some thing.
This is NOT what I am looking for.
This is something else."""
        test_file.write_text(file_content)
        from logtweet import is_string_in_filelines

        found = is_string_in_filelines(
            search_string,
            filepath=test_file.as_posix(),
        )

        assert found is False


