# -*- coding: utf-8 -*-

"""Test functions regarding creation of the tweet."""

import pytest  # type: ignore


class TestBuildPreamble(object):
    """Tests for `build_preamble` function."""

    @pytest.mark.parametrize(
        "heading_string, expected_return",
        [
            ("Day 1: October 16, 2019, Wednesday", "1/#100DaysOfCode"),
            ("Day 2: October 16, 2019, Wednesday", "2/#100DaysOfCode"),
            ("Day 10: October 16, 2019, Wednesday", "10/#100DaysOfCode"),
            ("Day 99: October 16, 2019, Wednesday", "99/#100DaysOfCode"),
            ("Day 100: October 16, 2019, Wednesday", "100/#100DaysOfCode"),
            ("Day 999: October 16, 2019, Wednesday", "999/#100DaysOfCode"),
        ],
    )
    def test_valid_heading(self, heading_string, expected_return):
        """Return the correct preamble for a given heading string."""
        from logtweet._content.build import build_preamble
        actual_return = build_preamble(heading_string)

        assert actual_return == expected_return

    @pytest.mark.parametrize(
        "heading_string",
        [
            "Off-Day: November 2, 2019, Saturday",  # No day number.
            "Day 1, October 16, 2019, Wednesday",  # Comma instead of colon.
            "Day 1, October 16: 2019, Wednesday",  # Colon in wrong place.
            "Day 1, October 16, 2019: Wednesday",  # Colon in wrong place.
        ],
    )
    def test_exception_invalid_heading_string_format(self, heading_string):
        """Raise exception for invalid formatted heading strings."""
        from logtweet._content.build import build_preamble
        with pytest.raises(ValueError, match=r"^Could not build preamble.*$"):
            build_preamble(heading_string)
