# -*- coding: utf-8 -*-

"""Functions related to shorten a link."""

import typing

import requests


def get_short_link(
    long_link: str,
    bitly_api_key: typing.Optional[str] = None,
) -> str:
    """
    Create short link.

    If a Bitly API key is passed, then the Bitly service is used to generate
    the short link. Otherwise it defaults to the URL shortener at
    `https://s.lpld.io`.

    Arguments:
        long_link (str): Long link to shorten.
        bitly_api_key (Optional[str]): API key for the Bit.ly service.
            See the `Bitly API documentation`_ on how to retrieve an API key.
            Default is `None`.

    Returns:
        str: Shortened link pointing to the same resource as the long link.

    .. _Bitly API documentation:
        https://dev.bitly.com/v4/#section/Application-using-a-single-account

    """
    # TODO: Split into separate functions for default and Bit.ly shortener.
    # TODO: Only return shortened link, if it actually shorter. At least when
    #       using the default link shortener. When using Bit.ly the user might
    #       want to have the analytical data, even if the link is not shorter.
    shortener_url = "https://s.lpld.io/create"
    headers = {}
    shortlink_key = "short"
    if bitly_api_key:
        shortener_url = "https://api-ssl.bitly.com/v4/shorten"
        headers["Authorization"] = f"Bearer {bitly_api_key}"
        shortlink_key = "link"
    payload = {"long_url": long_link}
    response = requests.post(shortener_url, json=payload, headers=headers)
    response.raise_for_status()
    response_data: typing.Dict[str, str] = response.json()
    return response_data[shortlink_key]
