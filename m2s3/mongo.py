"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
MongoDB module:
~~~~~~~~~~~~~~
{desc}
"""


import subprocess
from . import log


def fetch(data):
    """

    :param data:
    :return:
    """
    host, port = data['host'], data['port']
    user, passwd = data['user_name'], data['password']
    dbs = data['dbs']
    for db in dbs:
        _mongodump(host, port, user, passwd, db)


def _mongodump(host, port, user, passwd, db):
    """

    :param host:
    :param port:
    :param user:
    :param passwd:
    :param db:
    :return:
    """

    #
    log.msg_debug("mongodump - {host}, {port}, {db}"
                  .format(host=host, port=port, db=db))
    args = "mongodump --host {host}:{port} -d {db} -u {user} -p {passwd} " \
           "-o /tmp/m2s3/mongodump".format(host=host, port=port, db=db,
                                           user=user, passwd=passwd)
    # Make the actual call
    p = subprocess.Popen(args.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    #
    if p.returncode != 0:
        raise OSError("mongodump failed!. Reason: {reason}".format(reason=p.communicate()))
    log.msg_debug(p.communicate())