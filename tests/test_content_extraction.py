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

    @pytest.mark.parametrize(
        "subheading_text",
        [
            "Today's Progress",
            "Thoughts",
            "Link(s)",
        ],
    )
    def test_existing_subheaders(self, day_1_heading, subheading_text):
        """Extract existing sub-headers."""
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
            "Links",  # Missing parenthesis.
        ],
    )
    def test_not_existing_subheaders(self, day_1_heading, subheading_text):
        """Extract not-existing sub-headers."""

        from logtweet import get_day_subheading_by_text
        with pytest.raises(
            LookupError,
            match=r"^No subheading with text '{0}'.*".format(subheading_text),
        ):
            get_day_subheading_by_text(
                day_1_heading,
                subheading_text,
            )


class TestGetFirstLink(object):
    """Tests for `get_first_link` function."""

    @pytest.fixture
    def link_variation_soup(self):
        """Create soup object for example page."""
        from bs4 import BeautifulSoup
        page_content = """<html>
<body>
<h1>100 Days Of Code - Log</h1>
<h2>Day 1: October 16, 2019, Wednesday</h2>
<h3>Link(s)</h3>
<ol>
  <li><a href="http://example.com/1">Example Link 1</a></li>
  <li><a href="http://example.com/2">Example Link 2</a></li>
</ol>
<h2>Day 2: October 17, 2019, Thursday</h2>
<h3>Link(s)</h3>
<ol>
  <li><a href="">Example Link 3</a></li>
</ol>
<h2>Day 3: October 18, 2019, Friday</h2>
<h3>Link(s)</h3>
<ol>
  <li>Example Link 4</li>
</ol>
<h2>Day 4: October 19, 2019, Sunday</h2>
<h3>Link(s)</h3>
<ol>
</ol>
<h2>Day 5: October 20, 2019, Monday</h2>
<h3>Link(s)</h3>
<h2>Day 6: October 21, 2019, Tuesday</h2>
</body>
</html>"""
        return BeautifulSoup(page_content, "html.parser")

    def test_valid_link(self, link_variation_soup):
        """Test extraction of a valid link."""
        heading_date = date(2019, 10, 16)
        expected_link = "http://example.com/1"  # Valid link
        from logtweet import get_day_heading
        day_heading = get_day_heading(
            link_variation_soup,
            heading_date,
        )

        from logtweet import get_first_link
        extracted_link = get_first_link(day_heading)

        assert extracted_link == expected_link

    @pytest.mark.parametrize(
        "heading_date, expected_link",
        [
            (date(2019, 10, 17), None),  # Empty link address (href).
            (date(2019, 10, 18), None),  # List item but no actual link
            (date(2019, 10, 19), None),  # Missing list items
            (date(2019, 10, 20), None),  # Missing list element
            (date(2019, 10, 21), None),  # Missing link subheader
        ],
    )
    def test_invalid_links(
        self,
        link_variation_soup,
        heading_date,
        expected_link,
    ):
        """
        Test extraction of first link from the list of links.

        Different cases are provided by parametrization.
        """
        from logtweet import get_day_heading
        day_heading = get_day_heading(
            link_variation_soup,
            heading_date,
        )

        from logtweet import get_first_link
        with pytest.raises(LookupError):
            get_first_link(day_heading)


class TestGetTweetMessage(object):
    """Tests for the `get_tweet_message` function."""


