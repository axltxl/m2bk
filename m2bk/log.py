# -*- coding: utf-8 -*-

"""
m2bk.log
~~~~~~~~~~~~~

Handles local and system-wide logging into files.
System-wide messages are logged through logging.

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""


import sys
import logging
import logging.handlers
#from clint.textui import colored
from .const import PKG_NAME
from .utils import debug

from clint.textui.colored import white, red, cyan, yellow, green

# Globals
_logger = None
_log_lvl = 0
_stdout = False

def _set_lvl(lvl):
    if lvl == 0:
        return logging.DEBUG
    elif lvl == 1:
        return logging.INFO
    elif lvl == 2:
        return logging.WARNING
    elif lvl == 3:
        return logging.ERROR
    elif lvl >= 4:
        return logging.CRITICAL
    else:
        return logging.INFO


def init(threshold_lvl, quiet_stdout):
    """
    Initiate the log module

    :param threshold_lvl: messages under this level won't be issued/logged
    :param to_stdout: activate stdout log stream
    """
    global _logger, _log_lvl

    # translate lvl to those used by 'logging' module
    _log_lvl = _set_lvl(threshold_lvl)

    # logger Creation
    _logger = logging.getLogger(PKG_NAME)
    _logger.setLevel(_log_lvl)

    # create syslog handler and set level to info
    syslog_h = logging.handlers.SysLogHandler(address='/dev/log')
    #log_h = logging.FileHandler('/var/log/m2bk.log') # for later

    # Base message format
    base_fmt = '%(name)s - [%(levelname)s] - %(message)s'

    # set formatter
    syslog_fmt = logging.Formatter(base_fmt)
    syslog_h.setFormatter(syslog_fmt)
    # add Handler
    _logger.addHandler(syslog_h)

    # create stout handler
    if not quiet_stdout:
        global _stdout
        _stdout = True


def to_stdout(msg, *, colorf=green, bold=False):
    if _stdout:
        print(colorf(msg, bold=bold))

def msg(message):
    """
    Log a regular message

    :param message: the message to be logged
    """
    to_stdout(" --- {message}".format(message=message))
    if _logger:
        _logger.info(message)


def msg_warn(message):
    """
    Log a warning message

    :param message: the message to be logged
    """
    to_stdout(" (!) {message}".format(message=message), colorf=yellow, bold=True)
    if _logger:
        _logger.warn(message)


def msg_err(message):
    """
    Log an error message

    :param message: the message to be logged
    """
    to_stdout(" !!! {message}".format(message=message), colorf=red, bold=True)
    if _logger:
        _logger.error(message)


def msg_debug(message):
    """
    Log a debug message

    :param message: the message to be logged
    """
    if _log_lvl == logging.DEBUG:
        to_stdout(" (*) {message}".format(message=message), colorf=cyan)
        if _logger:
            _logger.debug(message)
