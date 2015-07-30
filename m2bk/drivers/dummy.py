# -*- coding: utf-8 -*-

"""
m2bk.drivers.dummy
~~~~~~~

Dummy backup driver

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

from .. import log

def load(**options):
    """
    Load this driver

    :param \*\*options: A variadic list of options
    """
    log.msg("Hello!, I am a dummy, so I won't do a thing!")

def dispose():
    """
    Perform cleanup
    """
    log.msg("Good bye!, I am a dummy, so I won't do a thing!")

def get_name():
    """
    Return this driver's name
    """
    return "dummy"

def backup_file(*, file, host):
    """
    Perform backup action

    :param file: Name of the file to be used by the driver
    :param host: Corresponding host name associated with file
    """
    log.msg("[{host}] Backing up file '{file}'".format(host=host,file=file))
