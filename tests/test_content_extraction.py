# -*- coding: utf-8 -*-

"""Test functions regarding content extraction."""

from datetime import date
from unittest.mock import patch

import pytest


class TestHeadingMatchesDate(object):
    """Tests for the `is_today` function."""

    @pytest.mark.parametrize(
        "heading_text, given_date, expected_return",
        [
            (
                "Day 1: October 16, 2019, Wednesday",
                date(year=2019, month=10, day=16),
                True,
            ),
            (
                # What's before the colon should not matter
                "Day 2: October 16, 2019, Wednesday",
                date(year=2019, month=10, day=16),
                True,
            ),
            (
                # What's before the colon should not matter
                "Day 10: October 16, 2019, Wednesday",
                date(year=2019, month=10, day=16),
                True,
            ),
            (
                # What's before the colon should not matter
                "Day 100: October 16, 2019, Wednesday",
                date(year=2019, month=10, day=16),
                True,
            ),
            (
                "Day 1: October 16, 2019, Wednesday",
                date(year=2018, month=10, day=16), # Year is off
                False,
            ),
            (
                "Day 1: October 16, 2019, Wednesday",
                date(year=2019, month=9, day=16),  # Month is off
                False,
            ),
            (
                "Day 1: October 16, 2019, Wednesday",
                date(year=2019, month=10, day=17),  # Day is off
                False,
            ),
        ],
    )
    def test_valid_inputs(
        self,
        heading_text,
        given_date,
        expected_return,
        monkeypatch,
    ):

        from logtweet import heading_matches_date
        actual_return = heading_matches_date(heading_text, given_date)

        assert actual_return == expected_return


class TestGetTodayHeading(object):
    """Tests for get_today_heding function."""

    def test_extraction_of_first_heading(self, example_soup):
        """Return Tag object with the expected string content."""
        with patch("logtweet.date") as mock_date:
            mock_date.today.return_value = date(2019, 10, 16)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            from logtweet import get_today_heading
            heading = get_today_heading(example_soup)

            from bs4.element import Tag
            assert isinstance(heading, Tag)
            assert heading.name == "h2"
            assert heading.string == "Day 1: October 16, 2019, Wednesday"

    def test_extraction_of_second_heading(self, example_soup):
        """Return Tag object with the expected string content."""
        with patch("logtweet.date") as mock_date:
            mock_date.today.return_value = date(2019, 10, 17)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            from logtweet import get_today_heading
            heading = get_today_heading(example_soup)

            from bs4.element import Tag
            assert isinstance(heading, Tag)
            assert heading.name == "h2"
            assert heading.string == "Day 2: October 17, 2019, Thursday"

    def test_exception_if_no_heading_for_today(self, example_soup):
        """Raises exception if heading for today not in soup."""
        with patch("logtweet.date") as mock_date:
            mock_date.today.return_value = date(2019, 10, 18)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            with pytest.raises(LookupError, match=r"^No heading found.*$"):
                from logtweet import get_today_heading
                get_today_heading(example_soup)


