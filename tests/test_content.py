# TODO: Add tests for `get_tweet_content` function.
# TODO: Test no link in list.

import pytest


class TestCalcMaxTweetMsgLen(object):
    """Test for `calc_max_tweet_msg_len` function."""

    def test_tweet_length_calc(self):
        preamble = "0123456789"
        link = "0123456789"
        from logtweet._content.build import make_tweet_content
        white_spaces_in_empty_content = make_tweet_content("", "", "")
        max_tweet_len = 100
        expected_max_len = (
            max_tweet_len
            - len(preamble)
            - len(link)
            - len(white_spaces_in_empty_content)
        )
        from logtweet.content import calc_max_tweet_msg_len

        actual_max_len = calc_max_tweet_msg_len(preamble, link, max_tweet_len)

        assert actual_max_len == expected_max_len
