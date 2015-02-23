# -*- coding: utf-8 -*-

"""
Copyright (c) Alejandro Ricoveri
m2bk: A command line tool to simplify MongoDB backups

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

---------------------------
shell execution wrapper module
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


