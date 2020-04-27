# -*- coding: utf-8 -*-

"""Tests for the ``source`` module."""


import pytest  # type: ignore


class TestGetLogContentFromSource(object):
    """Test the `get_log_content_from_source` function."""

    def test_valid_url_returns_content(
        self,
        valid_url,
        page_content,
        monkeypatch,
    ):
        def return_page_content(*args, **kwargs):
            return page_content
        from logtweet._source import online
        monkeypatch.setattr(online, "get_content_from_url", return_page_content)
        from logtweet.source import get_log_content_from_source

        returned_content = get_log_content_from_source(valid_url)

        assert returned_content == page_content

    def test_invalid_url_raises_exception(
        self,
        invalid_url,
    ):
        """
        Test invalid URL raises exception.

        I am not testing for any specific exceptions, because that is up to the
        implementation, i.e. depends on the lower level functions.

        """
        from logtweet.source import get_log_content_from_source

        with pytest.raises(Exception):
            get_log_content_from_source(invalid_url)
