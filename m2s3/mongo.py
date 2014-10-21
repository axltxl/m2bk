"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
MongoDB module:
~~~~~~~~~~~~~~
Make gzipped database backups through mongodump
"""


import os
import stat
import subprocess
import time
import tarfile
from . import log


def _make_tarfile(src_dir):
    """
    Make gzipped tarball from a source directory

    :param src_dir: Source directory
    """
    output_file = src_dir + ".tar.gz"
    log.msg("Tarballing {out}...".format(out=output_file))
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(src_dir, arcname=os.path.basename(src_dir))


def make_backup_file(data):
    """
    Backup all specified databases into a gzipped tarball

    :param data: list containing mongodb-related parameters
    """

    # Path to the mongodump executable
    mongodump = data['mongodump']

    # Output directory
    out = data['output_dir']

    # Host and port
    host = data['host']
    port = data['port']

    # The user and password for connecting to the databases
    user = data['user_name']
    passwd = data['password']

    # Create output directory if it does not exist
    if not os.path.exists(out):
        log.msg_debug("Output path '{output}' does not exist, creating it ..."
                      .format(output=out))
        # create the actual directory
        os.makedirs(out)
        # set folder permissions to 0770
        os.chmod(out, stat.S_IRWXU | stat.S_IRWXG)

    # The mongodump directory is going to have a name indicating
    # the UNIX timestamp corresponding to the current creation time
    #now = str(int(time.time()))
    now = time.strftime("%Y-%m-%d_%H%M", time.gmtime(time.time()))
    out_dir = "{out}/mongodump-{now}".format(out=out, now=now)
    log.msg_debug("Output directory: {out_dir}".format(out_dir=out_dir))

    # For each database specified, run mongodump on it
    for db in data['dbs']:
        _mongodump(mongodump, host, port, user, passwd, db, out_dir)

    # After all has been done, make a gzipped tarball from it
    _make_tarfile(out_dir)


def _mongodump(mongodump, host, port, user, passwd, db, out_dir):
    """
    Run mongodump on a database

    :param host: host name or IP address
    :param port: port
    :param user: user name
    :param passwd: password
    :param db: database name
    """

    # Log the call
    log.msg_debug("mongodump [{mongodump}] - {db}@{host}:{port} > {output}"
                  .format(mongodump=mongodump, host=host,
                          port=port, db=db, output=out_dir))

    # Prepare the call
    args = "{mongodump} --host {host}:{port} -d {db} -u {user} -p {passwd} " \
           "-o {output}".format(mongodump=mongodump, host=host, port=port,
                                db=db, user=user, passwd=passwd, output=out_dir)

    # Make the actual call to mongodump
    p = subprocess.Popen(args.split(),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait for the process to finish
    p.wait()
    log.msg_debug(p.communicate())

    # In this way, we will know what went wrong on mongodump
    if p.returncode != 0:
        raise OSError("mongodump failed!. Reason: {reason}"
                      .format(reason=p.communicate()))