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
from .. import log
from ..const import PKG_NAME

#
# Default values for variables within this driver
#
FTP_DEFAULT_PORT = 21
FTP_DEFAULT_HOST = 'localhost'
FTP_DEFAULT_USER = 'anonymous'
FTP_DEFAULT_PASS = ''
FTP_DEFAULT_PWD  = '/'

#
# Global variables
#
_ftp = None
_ftp_user = None
_ftp_pass = None
_ftp_host = None
_ftp_port = None
_ftp_pwd  = None

# Dry run mode
_dry_run = False

def load(**options):
    """
    Load this driver

    :param \*\*options: A variadic list of options
    """
    # Dry run mode
    global _dry_run; _dry_run = options.get('dry_run', False)

    # Set up global variables
    global _ftp_host, _ftp_port, _ftp_user, _ftp_pass, _ftp_pwd
    _ftp_host = options.get('host', FTP_DEFAULT_HOST)
    _ftp_port = options.get('port', FTP_DEFAULT_PORT)
    _ftp_user = options.get('user_name', FTP_DEFAULT_USER)
    _ftp_pass = options.get('password', FTP_DEFAULT_PASS)
    _ftp_pwd  = options.get('pwd', FTP_DEFAULT_PWD)

    # Log the thing prior to actual connection to FTP server
    log.msg("Attempting connection to ftp://{user}@{host}:{port}"
        .format(user=_ftp_user, host=_ftp_host, port=_ftp_port))

    # Connect to FTP server and log in
    global _ftp; _ftp = FTP()
    if not _dry_run:
        _ftp.connect(host=_ftp_host, port=_ftp_port)
    log.msg("Connection to FTP server successful!")

    log.msg("Logging in ...")
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

    if not _dry_run:
        # Change PWD to the one set by user
        _ftp.cwd(_ftp_pwd)

        # Move to the directory with name 'host' where the file
        # is going to  be stored at
        try:
            _ftp.cwd(host)
        except ftplib.error_perm:
            log.msg_warn("Destination directory at '/{pwd}/{dir}'"
                + " does not exist. I will proceed to create it.".format(pwd=_ftp_pwd, dir=host))
            _ftp.mkd(host); _ftp.cwd(host)

    # The actual STOR command to be sent to the FTP server
    store_cmd = "STOR {file}".format(file=os.path.basename(file))

    # Log the thing prior to action
    log.msg("[{host}] Storing file '{file}'".format(host=host,file=file))
    log.msg_debug("ftp {cmd}".format(cmd=store_cmd))

    # Store the file onto destination directory
    if not _dry_run:
        with open(file, 'rb') as f:
            _ftp.storbinary(store_cmd, f)

    # Log the thing
    log.msg("The file has been properly stored at: ftp://{host}:{port}/{pwd}/{dir}"
        .format(host=_ftp_host, port=_ftp_port, pwd=_ftp_pwd, dir=host))
