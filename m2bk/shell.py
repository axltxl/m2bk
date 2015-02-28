# -*- coding: utf-8 -*-

"""
m2bk.shell
~~~~~~~~~~

shell execution wrapper module

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import envoy  # envoy is awesome for this job
from . import utils, log


def run(cmd, **kwargs):
    """
    Execute a process

    :param cmd: name of the executable
    :param \*\*kwargs: arbitrary keyword arguments
    :raises OSError: if the execution of cmd fails
    """

    # command arguments
    args = kwargs.get('args', '')
    # execution timeout
    timeout = kwargs.get('timeout', 600)

    # tyoe checks
    utils.chkstr(cmd, 'cmd')
    utils.chkstr(args, 'args')

    # execute the command
    r = envoy.run("{cmd} {args}".format(cmd=cmd, args=args), timeout=timeout)
    # log stdout
    log.msg_debug("{cmd} > {stdout}".format(cmd=cmd, stdout=r.std_out.strip()))

     # In this way, we will know what went wrong on execution
    if r.status_code:
        log.msg_err("{cmd} > {stderr}".format(cmd=cmd, stderr=r.std_err.strip()))
        raise OSError("[{cmd}] execution failed!".format(cmd=cmd))


