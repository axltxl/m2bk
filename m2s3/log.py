"""
Copyright (c) Alejandro Ricoveri
m2s3: A mongodump straight to AWS S3

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------
Log messages:
~~~~~~~~~~~~~
Handles local and system-wide logging into files.
System-wide messages are logged through logging.
"""


import sys
import logging
from .const import PKG_NAME

# Globals
_logger = None


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


def init(threshold_lvl, to_stdout):
    """
    Initiate the log module

    :param threshold_lvl: messages under this level won't be issued/logged
    :param to_stdout: activate stdout log stream
    """
    global _logger

    # translate lvl to those used by 'logging' module
    log_lvl = _set_lvl(threshold_lvl)

    # logger Creation
    _logger = logging.getLogger(PKG_NAME)
    _logger.setLevel(log_lvl)

    # create syslog handler and set level to info
    syslog_h = logging.handlers.SysLogHandler(address='/dev/log')

    # Base message format
    base_fmt = '%(name)s - [%(levelname)s] - %(message)s'

    # set formatter
    syslog_fmt = logging.Formatter(base_fmt)
    syslog_h.setFormatter(syslog_fmt)
    # add Handler
    _logger.addHandler(syslog_h)

    # create stout handler
    if to_stdout:
        stdout_h = logging.StreamHandler(sys.stdout)
        #formatter
        stdout_fmt = logging.Formatter("* {fmt}".format(fmt=base_fmt))
        stdout_h.setFormatter(stdout_fmt)
        _logger.addHandler(stdout_h)


def msg(message):
    """
    Log a regular message

    :param message: the message to be logged
    """
    if _logger:
        _logger.info(message)


def msg_warn(message):
    """
    Log a warning message

    :param message: the message to be logged
    """
    if _logger:
        _logger.warn(message)


def msg_err(message):
    """
    Log an error message

    :param message: the message to be logged
    """
    if _logger:
        _logger.error(message)


def msg_debug(message):
    """
    Log a debug message

    :param message: the message to be logged
    """
    if _logger:
        _logger.debug(message)
