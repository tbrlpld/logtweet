# -*- coding: utf-8 -*-

"""Define methods for configuration of the app."""

from configparser import ConfigParser

import os


def get_config() -> ConfigParser:
    """
    Create config from possible config file locations.

    Possible config file locations:
        A `config.ini` can be located in the current working directory or at
        `~/.config/logtweet/config.ini`.

    Returns:
        ConfigParser: Initialized ConfigParser object.

    Raises:
        LookupError: Raised if no config file is found in any of the possible
            locations.

    """
    config = ConfigParser()
    possible_config_file_paths = (
        os.path.join(os.getcwd(), "config.ini"),
        os.path.expanduser("~/.config/logtweet/config.ini"),
    )
    # Check existence, use first existing
    for path in possible_config_file_paths:
        if os.path.exists(path):
            found_config = path
            break
    else:
        # This else is used if the for loop ends by running out of elements.
        raise LookupError(
            "No config file found. Please create a config file in one of the"
            + " following locations:\n"
            + "\n".join(possible_config_file_paths),
        )
    config.read(found_config)
    return config
