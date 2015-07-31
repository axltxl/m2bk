# -*- coding: utf-8 -*-

"""
m2bk.driver
~~~~~~~

Backup driver interface

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import importlib
from .utils import debug
from .const import PKG_NAME
from . import log

# Current driver in use
_driver = None

# List of supported drivers to load
VALID_DRIVERS = [
    'dummy',
    's3'
]

def get_name():
    return _driver.get_name()

def load(*, name="dummy", **kwargs):
    """
    Load a backup driver

    :param name: name of the backup driver to load
    :param \*\*kwargs: arbitrary keyword arguments
    :raises ValueError: if specified driver does not exist
    """
    global _driver

    #dry run
    dry_run = kwargs.get('dry_run', False)

    # Try to load specified driver
    if name in VALID_DRIVERS:
        # log the thing first
        log.msg_debug("Attempting to load driver: {d}".format(d=name))

        # List options that are passed to the driver
        options = kwargs.get('options', {})

        # Load the driver (which is actually a python
        # module inside the drivers directory)
        _driver = importlib.import_module(".drivers.{name}".format(name=name), __package__)
        if _driver:
            _driver.load(dry_run=dry_run, **options)
            log.msg_debug("Backup driver '{driver}' has been loaded successfully!"
                .format(driver=_driver.get_name()))
    else:
        raise ValueError('Invalid backup driver name')

def backup_file(*, file, host):
    """
    Perform backup action on set driver

    :param file: Name of the file to be used by the driver
    :param host: Corresponding host name associated with file
    """
    if _driver:
        log.msg_debug("[{driver}] Backing up file '{file}'"
            .format(driver=_driver.get_name(), file=file))
        _driver.backup_file(file=file, host=host)

def dispose():
    """
    Perform cleanup on set driver
    """
    if _driver:
        log.msg_debug("[{driver}] dispose".format(driver=_driver.get_name()))
        _driver.dispose()
