# -*- coding: utf-8 -*-

from .. import log

def load(**options):
    log.msg("Hello!, I am a dummy, so I won't do a thing!")

def dispose():
    log.msg("Good bye!, I am a dummy, so I won't do a thing!")

def get_name():
    return "dummy"

def backup_file(*, file, host):
    log.msg("[{host}] Backing up file '{file}'".format(host=host,file=file))
