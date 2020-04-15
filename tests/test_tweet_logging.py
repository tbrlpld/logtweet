# -*- coding: utf-8 -*-


class TestCreateTweetLoggingMsg(object):
    """Tests for ``create_tweet_logging_msg`` function."""

    def test_turn_multiline_tweet_into_single_line_logging_msg(self):
        tweet_content = "This is a\n\nmultiline\n\ntweet."
        expected_msg = "This is a  multiline  tweet."
        from logtweet import create_tweet_logging_msg

        actual_msg = create_tweet_logging_msg(tweet_content)

        assert actual_msg == expected_msg


