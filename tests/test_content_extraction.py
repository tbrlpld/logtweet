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


class TestGetDayHeading(object):
    """Tests for `get_day_heading`` function."""

    def test_extraction_of_first_heading(self, example_soup):
        """Return Tag object with the expected string content."""
        from logtweet import get_day_heading
        heading = get_day_heading(
            example_soup,
            heading_date=date(2019, 10, 16),
        )

        from bs4.element import Tag
        assert isinstance(heading, Tag)
        assert heading.name == "h2"
        assert heading.string == "Day 1: October 16, 2019, Wednesday"

    def test_extraction_of_second_heading(self, example_soup):
        """Return Tag object with the expected string content."""
        from logtweet import get_day_heading
        heading = get_day_heading(
            example_soup,
            heading_date=date(2019, 10, 17),
        )

        from bs4.element import Tag
        assert isinstance(heading, Tag)
        assert heading.name == "h2"
        assert heading.string == "Day 2: October 17, 2019, Thursday"

    def test_exception_if_no_heading_for_today(self, example_soup):
        """Raises exception if heading for today not in soup."""
        with pytest.raises(LookupError, match=r"^No heading found.*$"):
            from logtweet import get_day_heading
            get_day_heading(
                example_soup,
                heading_date=date(2019, 10, 18),
            )


class TestExtractDayNumberFromHeadingString(object):
    """Tests for `extract_day_number_from_heading_string` function."""

    @pytest.mark.parametrize(
        "heading_string, expected_return",
        [
            ("Day 1: October 16, 2019, Wednesday", 1),
            ("Day 2: October 16, 2019, Wednesday", 2),
            ("Day 10: October 16, 2019, Wednesday", 10),
            ("Day 99: October 16, 2019, Wednesday", 99),
            ("Day 100: October 16, 2019, Wednesday", 100),
            ("Day 999: October 16, 2019, Wednesday", 999),
        ],
    )
    def test_valid_heading(self, heading_string, expected_return):
        """Return the correct preamble for a given heading string."""
        from logtweet import extract_day_number_from_heading_string
        actual_return = extract_day_number_from_heading_string(heading_string)

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
        # heading_string = "Off-Day: November 2, 2019, Saturday"  # No day number
        # heading_string = "Day 1, October 16, 2019, Wednesday"  # Comma instead of colon.

        from logtweet import extract_day_number_from_heading_string
        with pytest.raises(
            ValueError,
            match=r"^Could not extract day number.*$",
        ):
            extract_day_number_from_heading_string(heading_string)


class TestGetDaySubheadingByText(object):
    """Test `get_day_subheading_by_text` function."""

    @pytest.fixture
    def day_1_heading(self, example_soup):
        from logtweet import get_day_heading
        return get_day_heading(example_soup, date(2019, 10, 16))

    @pytest.mark.parametrize(
        "subheading_text",
        [
            "Today's Progress",
            "Thoughts",
            "Link(s) to work",
        ],
    )
    def test_existing_subheaders(self, day_1_heading, subheading_text):
        """Extract existing progress sub-header."""
        from logtweet import get_day_subheading_by_text
        progress_subheading = get_day_subheading_by_text(
            day_1_heading,
            subheading_text,
        )

        from bs4.element import Tag
        assert isinstance(progress_subheading, Tag)
        assert progress_subheading.name == "h3"
        assert progress_subheading.text == subheading_text

    @pytest.mark.parametrize(
        "subheading_text",
        [
            "Todays Progress",  # Missing apostrophe.
            "thoughts",  # Not capitalized.
            "Links to work",  # Missing parenthesis.
        ],
    )
    def test_not_existing_subheaders(self, day_1_heading, subheading_text):
        """Extract existing progress sub-header."""
        from logtweet import get_day_subheading_by_text
        progress_subheading = get_day_subheading_by_text(
            day_1_heading,
            subheading_text,
        )

        assert progress_subheading is None
