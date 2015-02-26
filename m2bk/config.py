# -*- coding: utf-8 -*-

"""
m2bk.config
~~~~~~~~~~~

Configuration dictionary via a YAML file

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import yaml

# Base configuration object
_config = {}
_config_file_name = ""


def get_config_file_name():
    """
    Get the file name used for this config

    :return: a string with the name of the file
    """
    return _config_file_name


def get_config():
    """Get current configuration"""
    return _config


def clear():
    """Clear current configuration"""
    set_default({})


def get_entry(key):
    """
    Get a configuration entry

    :param key: key name
    :returns: mixed value
    :raises KeyError: if key has not been found
    :raises TypeError: if key is not str
    """
    if type(key) != str:
        raise TypeError("key must be str")
    if key not in _config:
        raise KeyError("Nonexistent entry '{key}'".format(key=key))
    return _config[key]


def set_entry(key, value):
    """
    Set a configuration entry

    :param key: key name
    :param value: value for this key
    :raises KeyError: if key is not str
    """
    if type(key) != str:
        raise KeyError('key must be str')
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
    :raises TypeError: if cfg is not a dict
    """
    global _config
    if type(cfg) != dict:
        raise TypeError('cfg must be dict')
    _config = cfg


def _list_merge(src, dest):
    """
    Merge the contents coming from src into dest

    :param src: source dictionary
    :param dest: destination dictionary
    """
    for k in src:
        if type(src[k]) != dict:
            dest[k] = src[k]
        else:
            # ---
            # src could have a key whose value is a list
            # and does not yet exist on dest
            if not k in dest:
                dest[k] = {}
            _list_merge(src[k], dest[k])


def set_from_file(file_name):
    """
    Merge configuration from a file with JSON data

    :param file_name: name of the file to be read
    :raises TypeError: if file_name is not str
    """
    if type(file_name) != str:
        raise TypeError('file_name must be str')
    global _config_file_name
    _config_file_name = file_name
    # Try to open the file and get the json data into a dictionary
    with open(file_name, "r") as file:
        data = yaml.load(file)
    # each value found will overwrite the same value in the config
    _list_merge(data, _config)

