# -*- coding: utf-8 -*-

"""Functions related to sending a tweet."""

import tweepy  # type: ignore


def send_tweet(tweet_content: str, twitter_config: dict) -> None:
    """
    Send tweet with given content.

    The sending requires valid Twitter access. Pass the twitter config as a
    dict-like object with the following keys:

    * "api_key",
    * "api_secret",
    * "access_token",
    * "access_secret".

    Arguments:
        tweet_content (str): Content of the tweet.
        twitter_config (dict): Dict-like object with above keys.

    """
    tweepy_api = get_tweepy_api(
        twitter_config["api_key"],
        twitter_config["api_secret"],
        twitter_config["access_token"],
        twitter_config["access_secret"],
    )
    # Send tweet
    tweepy_api.update_status(tweet_content)


def get_tweepy_api(
    api_key: str,
    api_secret: str,
    access_token: str,
    access_secret: str,
) -> tweepy.API:
    """
    Create authenticated Tweepy API.

    Requires twitter API access information.

    Arguments:
        api_key (str): Twitter API key
        api_secret (str): Twitter API secret
        access_token (str): Twitter API access token
        access_secret (str): Twitter API access secret

    Returns:
        tweepy.API: Authenticated tweepy API object.

    """
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    api.verify_credentials()  # Raises exception if not valid
    return api
