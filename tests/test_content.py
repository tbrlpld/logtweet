# TODO: Add tests for `get_tweet_content` function.
# TODO: Test no link in list.

import pytest  # type: ignore


class TestCalcMaxTweetMsgLen(object):
    """Test for `calc_max_tweet_msg_len` function."""

    @pytest.mark.parametrize(
        "preamble, link, max_tweet_len, expected_max_len",
        [
            ("", "", 0, -3),  # Test that 3 whitespace are always considered
            ("", "", 10, 7),  # Test that 3 whitespace are always considered
            ("", "", 100, 97),  # Test that 3 whitespace are always considered
            ("0123456789", "0123456789", 100, 77),
        ],
    )
    def test_msg_length_calc(
        self,
        preamble,
        link,
        max_tweet_len,
        expected_max_len,
    ):
        from logtweet.content import calc_max_tweet_msg_len

        actual_max_len = calc_max_tweet_msg_len(preamble, link, max_tweet_len)

        assert actual_max_len == expected_max_len
