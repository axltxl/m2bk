"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
MongoDB module:
~~~~~~~~~~~~~~
Make gzipped database backups via mongodump
"""


import os
import stat
import subprocess
import time
import tarfile
import sys
from . import log
from .const import (
    MONGODB_DEFAULT_HOST,
    MONGODB_DEFAULT_PORT,
    MONGODB_DEFAULT_MONGODUMP,
    MONGODB_DEFAULT_OUTPUT_DIR,
    MONGODB_DEFAULT_USER,
    MONGODB_DEFAULT_PWD
)


def _make_tarfile(src_dir):
    """
    Make gzipped tarball from a source directory

    :param src_dir: source directory
    :raises TypeError: if src_dir is not str
    """
    if type(src_dir) != str:
        raise TypeError('src_dir must be str')
    output_file = src_dir + ".tar.gz"
    log.msg("Wrapping tarball '{out}' ...".format(out=output_file))
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(src_dir, arcname=os.path.basename(src_dir))
    return output_file


def _chkstr(s, v):
    if type(s) != str:
        raise TypeError("{var} must be str".format(var=v))
    if not s:
        raise ValueError("{var} cannot be empty".format(var=v))


def make_backup_file(**kwargs):
    """
    Backup all specified databases into a gzipped tarball

    :param data: a list containing mongodb-related parameters
    :param \*\*kwargs: arbitrary keyword arguments
    :raises TypeError: if an argument in kwargs does not have the type expected
    :raises ValueError: if an argument within kwargs has an invalid value
    """

    # Path to the mongodump executable
    mongodump = kwargs.get('mongodump', MONGODB_DEFAULT_MONGODUMP)
    # Output directory
    out = kwargs.get('output_dir', MONGODB_DEFAULT_OUTPUT_DIR)
    # Host and port
    host = kwargs.get('host', MONGODB_DEFAULT_HOST)
    port = kwargs.get('port', MONGODB_DEFAULT_PORT)
    # The user and password for connecting to the databases
    user = kwargs.get('user_name', MONGODB_DEFAULT_USER)
    passwd = kwargs.get('password', MONGODB_DEFAULT_PWD)
    # databases
    dbs = kwargs.get('dbs', [])
    #dry run
    dry_run = kwargs.get('dry_run', False)

    # Type checks
    _chkstr(mongodump, 'mongodump')
    _chkstr(out, 'output_dir')
    _chkstr(host, 'host')
    _chkstr(user, 'user_name')
    _chkstr(passwd, 'password')
    if type(port) != int:
        raise TypeError('port must be int')
    if port < 1 and port > 65535: # check valid range in port
        raise ValueError('port must be between 1 and 65535')
    if type(dbs) != list or len(dbs) == 0:
        raise ValueError('dbs must be filled list')
    for db in dbs:
        if type(db) != str:
            raise TypeError('all values within dbs must be str')

    # Create output directory if it does not exist
    if not os.path.exists(out):
        log.msg_debug("Output path '{output}' does not exist, creating it ..."
                      .format(output=out))
        # create the actual root output directory
        os.makedirs(out)
        # set folder permissions to 0770
        os.chmod(out, stat.S_IRWXU | stat.S_IRWXG)

    # The mongodump directory is going to have a name indicating
    # the UNIX timestamp corresponding to the current creation time
    now = time.strftime("%Y-%m-%d_%H%M", time.gmtime(time.time()))
    out_dir = "{out}/mongodump-{host}-{now}".format(host=host, out=out, now=now)
    # create the current backup directory
    os.makedirs(out_dir)
    log.msg_debug("Output directory: {out_dir}".format(out_dir=out_dir))

    # For each database specified, run mongodump on it
    for db in dbs:
        _mongodump(mongodump, host, port, user, passwd, db, out_dir, dry_run)
    # After all has been done, make a gzipped tarball from it
    return _make_tarfile(out_dir)


def _mongodump(mongodump, host, port, user, passwd, db, out_dir, dry_run):
    """
    Run mongodump on a database

    :param host: server host name or IP address
    :param port: server port
    :param user: user name
    :param passwd: password
    :param db: database name
    :raises OSError: if mongodump process returns error
    """

    # Log the call
    log.msg("mongodump [{mongodump}] db={db} "
                  "mongodb://{user}@{host}:{port} > {output}"
                  .format(mongodump=mongodump, user=user, host=host,
                          port=port, db=db, output=out_dir))

    # Prepare the call
    args = "{mongodump} --host {host}:{port} -d {db} -u {user} -p {passwd} " \
           "-o {output}".format(mongodump=mongodump, host=host, port=port,
                                db=db, user=user, passwd=passwd, output=out_dir)

    if not dry_run:
        # Make the actual call to mongodump
        p = subprocess.Popen(args.split(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # wait for the process to finish
        p.wait()

        # Print stdout and stderr from the mongodump process
        stdout_data, stderr_data = p.communicate()
        stdout_str = stdout_data.decode(sys.stdout.encoding)
        stderr_str = stderr_data.decode(sys.stdout.encoding)
        log.msg_debug("{mongodump} > {stdout}"
                      .format(mongodump=mongodump, stdout=stdout_str))
        if stderr_str != '':
            log.msg_err("{mongodump} > {stderr}"
                        .format(mongodump=mongodump, stderr=stderr_str))

        # In this way, we will know what went wrong on mongodump
        if p.returncode != 0:
            raise OSError("mongodump failed!. Reason: {reason}"
                          .format(reason=p.communicate()))
