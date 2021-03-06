# -*- coding: utf-8 -*-

"""Functions related to extracting data from a 100DaysOfCode log."""

import datetime
import re
from typing import Tuple

import bs4  # type: ignore

from logtweet._content import exceptions


DATE_FORMAT = "%B %d, %Y"  # noqa: WPS323


def get_day_heading(
    soup: bs4.BeautifulSoup,
    heading_date: datetime.date,
) -> bs4.element.Tag:
    """
    Return today's heading element or None.

    Arguments:
        soup (BeautifulSoup): Soup object of log page parsed with
            BeautifulSoup.
        heading_date (date): ``datetime.date`` object for which the heading
            shall be extracted.

    Returns:
        Tag: Heading element representing today.
        None: If no heading element for today was found.

    Raises:
        LookupError: Raised if no heading element for today was found.

    """
    day_headings = soup.find_all("h2")
    for day in day_headings[::]:
        if heading_matches_date(day.text, heading_date):
            return day
    raise LookupError("No heading found for today!")


def heading_matches_date(
    day_heading_text: str,
    given_date: datetime.date,
) -> bool:
    """
    Check if given day heading represents the given date.

    Arguments:
        day_heading_text (str) : String to extract the date from. Expected
            format like this: "Day 1: October 16, 2019, Wednesday".
        given_date (date): datetime.date object to check the heading
            text against.

    Returns:
        bool: Expresses if the given day heading text represents the given
            date.

    """
    # Extract the date string
    # TODO: Create separate function for the date_string extraction.
    # A separate function makes this easier to test.
    date_string = re.sub(
        r"(.*: )(.*)(, .*day.*)",  # pattern to create groups
        r"\2",  # Return only second group
        day_heading_text,
    )
    # Convert to date object
    date_obj = datetime.datetime.strptime(date_string, DATE_FORMAT).date()

    return date_obj == given_date


def get_day_number_from_heading_string(heading_string: str) -> int:
    """
    Extract day number from heading string.

    >>> get_day_number_from_heading_string(
    ...    "Day 1: October 16, 2019, Wednesday",
    ... )
    1

    Arguments:
        heading_string (str): Day's log header string from which the day can be
            extracted. Expected format is something like
            `Day 1: October 16, 2019, Wednesday`.

    Returns:
        int: Day number string that was extracted from the heading string.

    Raises:
        ValueError: is raised if no day number could be extracted due to
            formatting issues.

    """
    day_str = re.sub(
        r"(Day\s)(\d+)(:.*)",
        r"\2",
        heading_string,
    )
    try:
        day = int(day_str)
    except ValueError:
        raise ValueError(
            "Could not extract day number."
            + " Check the formatting of the given `heading_string`.",
        )
    return day


def get_first_link(day_heading: bs4.element.Tag) -> str:
    """
    Extract the first link  URL from the list of the day's links.

    Expects the following structure after the day header:

    ::

        <h2>Day 1: October 16, 2019, Wednesday</h2>
        ...
        <h3>Link(s)</h3>
        <ol>
          <li><a href="http://example.com/1">Example Link 1</a></li>
          <li><a href="http://example.com/2">Example Link 2</a></li>
        </ol>

    For the given example, it would return "http://example.com/1".

    Arguments:
        day_heading (Tag): Day's log header element which is followed by the
            subheadings. The ``Link(s)`` subheading in turn needs to be
            followed by an ordered list. The link address (``href``) found in
            the anchor element of the first list item is returned.

    Returns:
        str: First link address found in the first list item.

    Raises:
        LookupError: is raised if no link could be found under the day's
            heading. This also includes anchor element with empty ``href``
            attribute.

    """
    link_address = ""
    link_heading = get_day_subheading_by_text(day_heading, "Link(s)")
    try:
        link_address = (
            link_heading.find_next_sibling(
                "ol",
            ).li.a.get("href")
        )
    except AttributeError:
        pass
    if not link_address:  # Catches empty link addresses and None
        raise LookupError(
            "No link extracted."
            + " Please check that a link list exists under the day's heading.",
        )
    return link_address


def get_day_subheading_by_text(
    day_heading: bs4.element.Tag,
    subheading_text: str,
) -> bs4.element.Tag:
    """
    Retrieve the next subheader (h3) element with the given text.

    This function only iterates over the following sibling's of the given
    ``day_heading`` until the next day heading (h2) is found.

    Arguments:
        day_heading (Tag): Tag element of a day's header. This is the
            starting point to look for following sibling subheaders.
        subheading_text (str): Content string for the searched subheader, which
            can be retrieved from the subheader element with
            ``subheader.text``.

    Returns:
        Tag: Found subheader element with given ``.text`` attribute.

    Raises:
        LookupError: if no subheader with the given ``.text`` attribute could
            be found after the given ``day_heading`` element and before the
            next.

    """
    # Go over the next siblings until the next day heading is found
    current_element = day_heading
    while True:
        next_sibling = current_element.next_sibling
        if not next_sibling or next_sibling.name == "h2":
            break
        if next_sibling.name == "h3" and next_sibling.text == subheading_text:
            return next_sibling
        current_element = next_sibling
    raise LookupError(
        "No subheading with text '{0}' could be found".format(subheading_text)
        + " after the day heading '{0}'!".format(day_heading),
    )


def get_progress_paragraphs(day_heading: bs4.element.Tag) -> Tuple[str, ...]:
    """
    Return all progress paragraphs that follow the given `day_heading`.

    Parameters
    ----------
    day_heading : bs4.element.Tag
        Day heading element after which the progress paragraphs should be
        returned.

    Returns
    -------
    Tuple[str, ...]
        Tuple containing all the strings of the progress paragraphs. Empty
        paragraphs are filtered. Tuple will never be empty. If no paragraphs
        with content are found, EmptyProgressParagraphsError is raised.

    # noqa: DAR402

    Raises
    ------
    LookupError
        When no day section header with the text `"Today's Progress"` can be
        found.
    NoProgressPargraphsError
        When no paragraph elements after the progress section header are found.
    EmptyProgressParagraphsError
        When no content could be extracted out of the existing paragraph
        elements following the progress section header.

    """
    progress_heading = get_day_subheading_by_text(
        day_heading,
        "Today's Progress",
    )

    # This could be integrated into the while loop, but I like the readability
    # better right now.
    possible_paragraph = progress_heading.find_next_sibling()
    if possible_paragraph is None or possible_paragraph.name != "p":
        raise exceptions.NoProgressPargraphsError

    paragraph_contents = []
    while (possible_paragraph is not None and possible_paragraph.name == "p"):
        current_paragraph = possible_paragraph

        paragraph_contents.append(current_paragraph.text)

        possible_paragraph = current_paragraph.find_next_sibling()

    # Remove empty items
    paragraph_contents = list(
        filter(lambda item: item != "", paragraph_contents),  # noqa: WPS110
    )
    if not paragraph_contents:
        raise exceptions.EmptyProgressParagraphsError

    return tuple(paragraph_contents)
