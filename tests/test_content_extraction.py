# -*- coding: utf-8 -*-

"""Test functions regarding content extraction."""

from datetime import date

from bs4 import BeautifulSoup
import pytest


class TestIsToday(object):
    """Tests for the `is_today` function."""

    @pytest.mark.parametrize(
        "heading_text, mock_today, expected_return",
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
                date(year=2018, month=10, day=16),  # Year is off
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
        mock_today,
        expected_return,
        monkeypatch,
    ):
        import logtweet
        monkeypatch.setattr(logtweet, "TODAY", mock_today)

        from logtweet import is_today
        is_today_return = is_today(heading_text)

        assert is_today_return == expected_return

    @pytest.mark.parametrize(
        "mock_today, offset, expected_return",
        [
            (
                date(year=2019, month=10, day=17),
                -1,
                True,
            ),
            (
                date(year=2019, month=10, day=15),
                1,
                True,
            ),
            (
                date(year=2018, month=10, day=16),
                365,
                True,
            ),
            (
                date(year=2020, month=10, day=16),
                -366,  # 2020 is a leap year
                True,
            ),
            (
                date(year=2019, month=10, day=15),
                0,
                False,
            ),
        ],
    )
    def test_different_offsets(
        self,
        mock_today,
        offset,
        expected_return,
        monkeypatch,
    ):
        heading_text = "Day 1: October 16, 2019, Wednesday"

        import logtweet
        monkeypatch.setattr(logtweet, "TODAY", mock_today)

        from logtweet import is_today
        is_today_return = is_today(heading_text, offset)

        assert is_today_return == expected_return


class TestGetTodayHeading(object):
    """Tests for get_today_heding function."""

    @pytest.fixture
    def example_soup():
        """Create soup object for example page."""
        page_content = """<html>
    <body>
    <h1>100 Days Of Code - Log</h1>
    <h2>Day 1: October 16, 2019, Wednesday</h2>
    <h3>Today&#39;s Progress</h3>
    <p>Gone through first bit of Flask introduction and set up the basic project structure in #100DayOfWebInPython.
    Also, enabled Markdown formatting for posts in the Flaskr blog app (as suggested in the &#34;Keep Developing&#34; section of the Flask tutorial).</p>
    <h3>Thoughts</h3>
    <p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
    <p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
    <h3>Link(s) to work</h3>
    <ol>
      <li><a href="http://example.com/1">Example Link 1</a></li>
      <li><a href="http://example.com/2">Example Link 2</a></li>
      <li><a href="http://example.com/3">Example Link 3</a></li>
    </ol>
    </body>
    </html>"""
        return BeautifulSoup(page_content, "html.parser")

    def test_get_today_heading(monkeypatch, example_soup):
        import logtweet
        def mock_is_today(*args, **kwargs):
            """
            Return true.

            Because the example soup only contains one day, this patch can be used
            to override the usually used test to see if the date matches today.

            Returns:
                bool: Always True.

            """
            return True
        monkeypatch.setattr(logtweet, "is_today", mock_is_today)

        from logtweet import get_today_heading
        heading = get_today_heading(example_soup)

        assert heading.name == "h2"
        assert heading.string == "Day 1: October 16, 2019, Wednesday"
