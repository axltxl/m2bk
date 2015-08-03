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


def run(cmd, *, args='', timeout=600):
    """
    Execute a process

    :param cmd(str): name of the executable
    :param args(str, optional): arbitrary arguments
    :param timeout(int, optional): Execution timeout
    :raises OSError: if the execution of cmd fails
    """

    # type checks
    utils.chkstr(cmd, 'cmd')
    utils.chkstr(args, 'args')

    # execute the command
    r = envoy.run("{cmd} {args}".format(cmd=cmd, args=args), timeout=timeout)
    # log stdout
    log.msg_debug("{cmd} > {stdout}".format(cmd=cmd, stdout=r.std_out.strip()))

    # In this way, we will know what went wrong on execution
    if r.status_code:
        log.msg_err("{cmd} > {stderr}".format(cmd=cmd,
                                              stderr=r.std_err.strip()))
        raise OSError("[{cmd}] execution failed!".format(cmd=cmd))
