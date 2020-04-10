# -*- coding: utf-8 -*-

"""Test functions regarding content extraction."""

from datetime import date

from bs4 import BeautifulSoup
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

    # TODO: Make test actual extraction of the heading for a given day.
    # Mocking datetime.date.today is messy somehow. It might be easier
    # to adjust the function under test. Make the date to check against
    # an input argument. This could default to datetime.date.today.
    # This option should make the function a lot easier to test.
    @pytest.fixture
    def example_soup(self):
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

    def test_extraction_of_first_heading(self, monkeypatch, example_soup):
        """Returns Tag object with the expected string content."""
        import logtweet
        def always_true(*args, **kwargs):
            return True
        monkeypatch.setattr(logtweet, "heading_matches_date", always_true)

        from logtweet import get_today_heading
        heading = get_today_heading(example_soup)

        from bs4.element import Tag
        assert isinstance(heading, Tag)
        assert heading.name == "h2"
        assert heading.string == "Day 1: October 16, 2019, Wednesday"

    def test_exception_if_is_today_always_false(
        self,
        monkeypatch,
        example_soup,
    ):
        """
        In case that `heading_matches_date` returns false on every heading (this is mocked
        here) the function should raise an exception that no heading was found.
        """
        import logtweet
        def always_false(*args, **kwargs):
            return False
        monkeypatch.setattr(logtweet, "heading_matches_date", always_false)

        with pytest.raises(LookupError, match=r"^No heading found.*$"):
            from logtweet import get_today_heading
            get_today_heading(example_soup)


# Just for reference
# <html>
#     <body>
#     <h1>100 Days Of Code - Log</h1>
#     <h2>Day 1: October 16, 2019, Wednesday</h2>
#     <h3>Today&#39;s Progress</h3>
#     <p>Gone through first bit of Flask introduction and set up the basic project structure in #100DayOfWebInPython.
#     Also, enabled Markdown formatting for posts in the Flaskr blog app (as suggested in the &#34;Keep Developing&#34; section of the Flask tutorial).</p>
#     <h3>Thoughts</h3>
#     <p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
#     <p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
#     <h3>Link(s) to work</h3>
#     <ol>
#       <li><a href="http://example.com/1">Example Link 1</a></li>
#       <li><a href="http://example.com/2">Example Link 2</a></li>
#       <li><a href="http://example.com/3">Example Link 3</a></li>
#     </ol>
#     </body>
# </html>
