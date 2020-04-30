# -*- coding: utf-8 -*-

"""Functions related to extracting data from a 100DaysOfCode log."""

import datetime
import re

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
    link_address = None
    link_heading = get_day_subheading_by_text(day_heading, "Link(s)")
    try:
        link_address = (
            link_heading.find_next_sibling(  # type: ignore
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


def get_progress_paragraphs(day_heading: bs4.element.Tag):
    """
    Return all progress paragraphs that follow the given `day_heading`.

    # TODO: Document function

    """
    progress_heading = get_day_subheading_by_text(
        day_heading,
        "Today's Progress",
    )

    next_sibling = progress_heading.find_next_sibling()
    if next_sibling is None or next_sibling.name != "p":
        raise exceptions.NoProgressPargraphsError

    paragraph_contents = []
    while (next_sibling is not None and next_sibling.name == "p"):
        current_paragraph = next_sibling

        paragraph_contents.append(current_paragraph.text)

        next_sibling = current_paragraph.find_next_sibling()

    # Remove empty items
    paragraph_contents = list(
        filter(lambda item: item != "", paragraph_contents),  # noqa: WPS110
    )
    if not paragraph_contents:
        raise exceptions.EmptyProgressParagraphsError

    return tuple(paragraph_contents)


def get_tweet_message(day_heading: bs4.element.Tag, max_len: int) -> str:
    """
    Extract the tweet content from the paragraphs after content heading.

    Arguments:
        day_heading (Tag): Heading tag element for today.
        max_len (int): Maximum length of tweet message.

    Returns:
        str: Tweet message with a maximum length of max_len

    Raises:
        LookupError: is raised if no content heading is found or the extracted
            message is empty.

    # TODO: Refactor to return all progress pargraphs. Have a separate function
    #       handle the the shortening to the maximum length. This makes the
    #       separation between extraction and building cleaner.

    """
    # Grab today's content heading
    content_heading = get_day_subheading_by_text(
        day_heading,
        "Today's Progress",
    )
    # Loop over the next siblings until you find something
    # that is not a paragraph. Extract content from the paragraphs until
    # maximum tweet length is reached.
    current_element = content_heading
    tweet_message = ""
    while True:
        possible_content = tweet_message
        next_sibling = current_element.find_next_sibling()
        if not next_sibling or next_sibling.name != "p":
            # Leave loop if no more siblings (end of page) or not a paragraph.
            break
        current_element = next_sibling

        # TODO: Separate function to concatenate message content
        possible_content = "{existing_content}\n\n{new_content}".format(
            existing_content=possible_content,
            new_content=current_element.text,
        ).strip()

        if len(possible_content) > max_len:
            # When possible content is longer than maximum before any thing is
            # extracted, a special error is raised to allow explicit handling
            # of this issue. This can go unhandled so that the user becomes
            # aware of this issue and can adjust the content in the log.
            if not tweet_message:
                raise ValueError(
                    "The first paragraph is too long!"
                    + " Maximum length: {}".format(max_len)
                    + " Extracted content: '{}'".format(possible_content)
                )
            break
        tweet_message = possible_content

    if not tweet_message:
        raise LookupError("No message found that could be tweeted!")
    return tweet_message
