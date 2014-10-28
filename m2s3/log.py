"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
Log messages:
~~~~~~~~~~~~~
Handles local and system-wide logging into files.
System-wide messages are logged through syslog.
"""


#TODO replace log with logging https://docs.python.org/3.4/howto/logging.html#logging-basic-tutorial
import syslog

# Globals
threshold = 0
debug = __debug__


def msg(message, lvl=0):
    """
    Logs a single message

    :param message: the message string itself
    :param lvl: message priority level
    """

    # The message would be logged only if its level
    # is equal or greater than the established log threshold
    if lvl >= threshold:
        syslog_prio = 0  # syslog priority
        if lvl == -1:
            syslog_prio = syslog.LOG_DEBUG
        elif lvl == 0:
            syslog_prio = syslog.LOG_INFO
        elif lvl == 1:
            syslog_prio = syslog.LOG_WARNING
        elif lvl >= 2:
            syslog_prio = syslog.LOG_ERR

        # Post the message into syslog
        syslog.syslog(syslog_prio, message)


def msg_warn(message):
    """
    Log a warning message

    :param message: the message to be logged
    """
    msg(_fmt('warn', message), 1)


def msg_err(message):
    """
    Log an error message

    :param message: the message to be logged
    """
    msg(_fmt('error', message), 2)


def msg_debug(message):
    """
    Log a debug message

    :param message: the message to be logged
    """
    if debug:
        msg(_fmt('debug', message), -1)


def _fmt(prefix, message):
    """
    Format a message

    :param message: the message to be formatted
    :return: formatted string
    """
    return "[{prefix}] -- {msg}".format(prefix=prefix.upper(), msg=message)