# -*- coding: utf-8 -*-

"""
m2bk.drivers.ftp
~~~~~~~

FTP driver

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import os
import ftplib
from ftplib import FTP
from .. import log, utils
from ..const import PKG_NAME

#
# Global variables
#
_ftp = None
_ftp_user = None
_ftp_pass = None
_ftp_host = None
_ftp_port = None
_ftp_pwd = None

# Dry run mode
_dry_run = False


def load(*,
         host='localhost',
         port=21,
         user_name='anonymous',
         password='',
         pwd='/',
         dry_run=False,
         **kwargs):
    """
    Load this driver

    :param \*\*options: A variadic list of options
    """
    # Dry run mode
    global _dry_run
    _dry_run = dry_run

    # Set up global variables
    global _ftp_host, _ftp_port, _ftp_user, _ftp_pass, _ftp_pwd
    _ftp_host = host
    _ftp_port = port
    _ftp_user = str(user_name)
    _ftp_pass = str(password)

    # Type checks
    utils.chkstr(_ftp_host, 'host')
    utils.chkstr(_ftp_user, 'user_name')
    utils.chkstr(_ftp_pass, 'password')
    utils.chkstr(pwd, 'pwd')

    # Set initial PWD
    _ftp_pwd = os.path.join('/', pwd)

    # Check port
    if type(port) != int:
        raise TypeError('port must be int')
    # check valid range in port
    if port < 1 or port > 65535:
        raise ValueError('port must be between 1 and 65535')

    # Log the thing prior to actual connection to FTP server
    log.msg("Attempting connection to ftp://{user}@{host}:{port}"
            .format(user=_ftp_user, host=_ftp_host, port=_ftp_port))

    # Connect to FTP server and log in
    global _ftp
    _ftp = FTP()

    if not _dry_run:
        _ftp.connect(host=_ftp_host, port=_ftp_port)
    log.msg("Connection to FTP server successful!")

    # Log in
    log.msg("Logging in as '{usr}' ...".format(usr=user_name))
    if not _dry_run:
        _ftp.login(user=_ftp_user, passwd=_ftp_pass)
    log.msg("Authentication against FTP server successful!")


def dispose():
    """
    Perform cleanup
    """
    if _ftp:
        log.msg_warn("Closing FTP connection")
        _ftp.close()


def get_name():
    """
    Return this driver's name
    """
    return "ftp"


def backup_file(*, file, host):
    """
    Perform backup action

    :param file: Name of the file to be used by the driver
    :param host: Corresponding host name associated with file
    """

    # Final destination directory
    dest_path = os.path.join(_ftp_pwd, host)

    if not _dry_run:
        # Move to the directory with name 'host' where the file
        # is going to  be stored at
        try:
            _ftp.cwd(dest_path)
        except ftplib.error_perm:
            log.msg_warn("Destination directory at '{dst}'" \
                         " does not exist. I will proceed to create it."
                         .format(dst=dest_path))
            _ftp.mkd(dest_path)  # Create new directory
            _ftp.cwd(dest_path)  # Move to the new directory

    # The actual STOR command to be sent to the FTP server
    store_cmd = "STOR {file}".format(file=os.path.basename(file))

    # Log the thing prior to action
    log.msg("[{host}] Storing file '{file}'".format(host=host, file=file))
    log.msg_debug("ftp {cmd}".format(cmd=store_cmd))

    # Store the file onto destination directory
    if not _dry_run:
        with open(file, 'rb') as f:
            _ftp.storbinary(store_cmd, f)

    # Log the thing
    log.msg("The file has been properly stored at: " \
            "ftp://{host}:{port}{pwd}{dir}"
            .format(host=_ftp_host, port=_ftp_port, pwd=_ftp_pwd, dir=host))
