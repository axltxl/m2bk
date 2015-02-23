# -*- coding: utf-8 -*-

"""
Test for: command line arguments
"""

from nose.tools import eq_, assert_raises
from m2bk import app, config, const
import os


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
    # ---
    # Test whether -c works as --config
    eq_(_get_arg_cfg_file_name('-c', f1),
        _get_arg_cfg_file_name('--config', f1),
        msg="-c and --config are not capturing the expected file name")
    # ---
    # Test -c and --config with more than one value
    assert_raises(SystemExit, app.init_parsecmdline, ['-c', f1, f2])
    # absolute path is expected for f1
    eq_(config.get_config_file_name(), os.path.abspath(f1),
        msg="Unexpected file, it should be within its absolute path")
    # ---
    # test when several config directives are specified
    try:
        app.init_parsecmdline(['-c', f1, '--config', f2, '-c', f3])
    except FileNotFoundError:
        pass
    # file name should be f3
    eq_(config.get_config_file_name(), os.path.abspath(f3),
        msg="The last --config/-c argument should be the one whose file name"
            "should be captured")


def test_args_noargs():
    # Test whether m2bk tries to use default config file
    # when no arguments are present
    try:
        app.init_parsecmdline()
    except FileNotFoundError:
        pass
    eq_(config.get_config_file_name(), const.CONF_DEFAULT_FILE,
        msg="CONF_DEFAULT_FILE expected")
