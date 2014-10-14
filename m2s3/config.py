"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
JSON-based configuration:
~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration dictionary via a JSON file
"""

import json

# Base configuration object
_config = {}


def get_entry(key):
    """
    Get a configuration entry

    :param key: key name
    :returns: mixed value
    """
    if key in _config:
        return _config[key]
    return 0  # temp


def set_entry(key, value):
    """
    Set a configuration entry

    :param key: key name
    :param value: value for this key
    """
    _config[key] = value


def set_default(cfg):
    """
    Set initial configuration values

    This is used mostly for setting up an initial set of values
    before using the actual config set. It is important to know
    that using this function would result in a total overwrite of
    the whole config set, so it is only meant to be used before
    anything.

    :param cfg: dictionary containing the initial values
    """
    global _config
    _config = cfg


def set_from_file(file_name):
    """
    Merge configuration from a file with JSON data

    :param file_name: name of the file to be read
    """
    try:
        # Try to open the file and get the json data into a dictionary
        with open(file_name, "r") as file:
            data = json.loads(file.read().replace('\n', ''))
        # each value found will overwrite the same value in the config
        for k in data:
            _config[k] = data[k]
    #TODO a better exception handling is needed here
    except Exception:
        pass
