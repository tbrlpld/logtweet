# -*- coding: utf-8 -*-

"""Test functions regarding creation of the tweet."""

import pytest  # type: ignore


class TestMakePreamble(object):
    """Tests for `make_preamble` function."""

    @pytest.mark.parametrize(
        "day_number, expected_return",
        [
            (1, "1/#100DaysOfCode"),
            (2, "2/#100DaysOfCode"),
            (10, "10/#100DaysOfCode"),
            (99, "99/#100DaysOfCode"),
            (100, "100/#100DaysOfCode"),
            (999, "999/#100DaysOfCode"),
        ],
    )
    def test_valid_int_inputs(self, day_number, expected_return):
        """Return the correct preamble for a given heading string."""
        from logtweet._content.build import make_preamble
        actual_return = make_preamble(day_number)

        assert actual_return == expected_return

    @pytest.mark.parametrize(
        "day_number, received_type",
        [
            ("1", "str"),
        ],
    )
    def test_exception_if_invalid_day_number_type(
        self,
        day_number,
        received_type,
    ):
        """Raise exception for invalid formatted heading strings."""
        from logtweet._content.build import make_preamble
        with pytest.raises(
            TypeError,
            match=r"^Expected 'int', got '{0}'.*$".format(received_type),
        ):
            make_preamble(day_number)


class TestMakeTweetContent(object):
    """Tests for `make_tweet_content` function."""

    @pytest.mark.parametrize(
        "preamble, message, link, expected_tweet_content",
        [
            ("", "", "", " \n\n"),  # Testing the white space
            ("preamble", "message", "link", "preamble message\n\nlink"),
            (
                "preamble",
                "messages first line\nmessages second line.",
                "link",
                "preamble messages first line\nmessages second line.\n\nlink"
            ),
        ],
    )
    def test_tweet_message_format(
        self,
        preamble,
        message,
        link,
        expected_tweet_content,
    ):
        preamble = "preamble"
        message = "message"
        link = "link"
        expected_tweet_content = "preamble message\n\nlink"
        from logtweet._content.build import make_tweet_content

        actual_tweet_content = make_tweet_content(preamble, message, link)

        assert actual_tweet_content == expected_tweet_content


class TestJoinStringsToMaxLen(object):
    """Test `join_strings_to_max_len` function."""

    def test_first_string_longer_than_max(self):
        """First string longer than max."""
        strings = ["This is the string"]
        from logtweet._content.exceptions import StringJoiningError
        from logtweet._content.build import join_strings_to_max_len

        with pytest.raises(
            StringJoiningError,
            match=r"^First string longer than maximum length",
        ):
            join_strings_to_max_len(strings, max_len=1)


    # def test_single_string_list_to_string(self):
    #     """Takes list with single string."""
    #     strings = ["This is the string"]
    #     expected = "This is the string"
    #     from logtweet._content.build import join_strings_to_max_len

    #     actual = join_strings_to_max_len(strings, max_len=len(expected))

    #     assert actual == expected

    # def test_single_string_tuple_to_string(self):
    #     """Takes tuple with single string."""
    #     strings = ("This is the string")
    #     expected = "This is the string"
    #     from logtweet._content.build import join_strings_to_max_len

    #     actual = join_strings_to_max_len(strings, max_len=len(expected))

    #     assert actual == expected


    # TEST: Second string longer than max
    # TEST: Define separator between strings
