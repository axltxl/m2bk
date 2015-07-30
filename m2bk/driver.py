# -*- coding: utf-8 -*-

import importlib
from .utils import debug
from .const import PKG_NAME
from . import log

_driver = None

def get_name():
    return _driver.get_name()

def load(*, name="dummy", **kwargs):
    global _driver

    #dry run
    dry_run = kwargs.get('dry_run', False)

    #
    valid_drivers = ['dummy', 's3']
    if name not in valid_drivers:
        raise ValueError('Invalid backup driver name')

    #
    options = kwargs.get('options', {})

    #
    _driver = importlib.import_module(".drivers.{name}".format(name=name), __package__)

    #
    if _driver:
        _driver.load(dry_run=dry_run, **options)
        log.msg_debug("Backup driver '{driver}' has been loaded successfully!"
            .format(driver=_driver.get_name()))

def backup_file(*, file, host):
    log.msg_debug("[{driver}] Backing up file '{file}'"
        .format(driver=_driver.get_name(), file=file))
    if _driver:
        _driver.backup_file(file=file, host=host)

def dispose():
    log.msg_debug("[{driver}] dispose".format(driver=_driver.get_name()))
    if _driver:
        _driver.dispose()
