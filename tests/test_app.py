"""
Test for: command line arguments
"""

from nose.tools import eq_
from m2s3 import app, config, const
import os

# Test whether a relative file specification is well interpreted
# Test invalid arguments

#
# Command line tests
#


def _get_arg_cfg_file_name(arg, filename):
    try:
        app.init_parsecmdline([arg, filename])
    except FileNotFoundError:
        pass
    return config.get_config_file_name()


def test_args_config():
    # file names
    f1 = 'f1.txt'
    f2 = 'f2.txt'
    f3 = 'f3.txt'

    # Test whether -c works as --config
    eq_(_get_arg_cfg_file_name('-c', f1),
                  _get_arg_cfg_file_name('--config', f1))

    # Test -c and --config with more than one value
    try:
        app.init_parsecmdline(['-c', f1, f2])
    except FileNotFoundError:
        pass
    # absolute path is expected for f1
    eq_(config.get_config_file_name(), os.path.abspath(f1))

    # test when several config directives are specified
    try:
        app.init_parsecmdline(['-c', f1, '--config', f2, '-c', f3])
    except FileNotFoundError:
        pass
    # file name should be f3
    eq_(config.get_config_file_name(), os.path.abspath(f3))


def test_args_noargs():
    # Test whether m2s3 tries to use default config file
    # when no arguments are present
    try:
        app.init_parsecmdline()
    except FileNotFoundError:
        pass
    eq_(config.get_config_file_name(), const.CONF_DEFAULT_FILE)