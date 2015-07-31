# -*- coding: utf-8 -*-

"""
m2bk.drivers.s3
~~~~~~~

Backup files on a S3 bucket

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import boto
import ntpath
from .. import log
from ..const import (
    AWS_DEFAULT_ACCESS_KEY,
    AWS_DEFAULT_ID,
    AWS_S3_DEFAULT_BUCKET_NAME
)

# Dry run mode
_dry_run = False

# AWS-specific options
_aws_access_key_id = None
_aws_secret_access_key = None
_bucket_name = None
_boto_conn = None

def load(**options):
    """
    Load this driver

    :param \*\*options: A variadic list of options
    """
    global _dry_run
    global _aws_access_key_id, _aws_secret_access_key, _bucket_name, _boto_conn

    #dry run
    _dry_run = options.get('dry_run', False)

    # AWS parameters from kwargs
    _aws_id = options.get('aws_id', AWS_DEFAULT_ID)
    _aws_access_key = options.get('aws_access_key', AWS_DEFAULT_ACCESS_KEY)
    if type(_aws_id) != str:
        raise TypeError('aws_id must be str')
    if type(_aws_access_key) != str:
        raise TypeError('aws_access_key must be str')

    # Check the bucket name before doing anything
    _bucket_name = options.get('s3_bucket', AWS_S3_DEFAULT_BUCKET_NAME)
    if type(_bucket_name) != str:
        raise TypeError('s3_bucket must be str')
    if not _bucket_name:
        raise ValueError("s3_bucket cannot be empty")

    # Connect to S3 service
    log.msg("Connecting to Amazon S3 Service")
    if not _aws_id and not _aws_access_key:
        log.msg_warn('No AWS credentials given. Assuming access via IAM role')
        if not _dry_run:
            _boto_conn = boto.connect_s3()
    elif not _aws_id or not _aws_access_key:
        if _aws_id:
            raise ValueError("aws_id given with no aws_access_key")
        else:
            raise ValueError("aws_access_key given with no aws_id")
    elif not _dry_run:
        _boto_conn = boto.connect_s3(aws_access_key_id=aws_id,
                               aws_secret_access_key=aws_key)
    log.msg("Connected to AWS S3 service successfully!")

def dispose():
    """
    Perform cleanup
    """
    pass

def get_name():
    """
    Return this driver's name
    """
    return "s3"


def backup_file(*, file, host):
    """
    Backup a file on S3

    :param file: full path to the file to be backed up
    :param host: this will be used to locate the file on S3
    :raises TypeError: if an argument in kwargs does not have the type expected
    :raises ValueError: if an argument within kwargs has an invalid value
    """

    # If the destination bucket does not exist, create one
    try:
        if not _dry_run:
            bucket = conn.get_bucket(_bucket_name)
    except boto.exception.S3ResponseError:
        log.msg_warn("Bucket '{bucket_name}' does not exist!, creating it..."
                     .format(bucket_name=_bucket_name))
        if not _dry_run:
            bucket = conn.create_bucket(_bucket_name)
        log.msg("Created bucket '{bucket}'".format(bucket=_bucket_name))

    # The key is the name of the file itself who needs to be stripped
    # from its full path
    key_path = "{key}/{file}".format(key=host, file=ntpath.basename(file))

    # Create a new bucket key
    if not _dry_run:
        k = boto.s3.key.Key(bucket)
        k.key = key_path

    # Upload the file to Amazon
    log.msg("Uploading '{key_path}' to bucket '{bucket_name}' ..."
            .format(key_path=key_path, bucket_name=_bucket_name))

    # It is important to encrypt the data on the server side
    if not _dry_run:
        k.set_contents_from_filename(file, encrypt_key=True)

    # Log the thing
    log.msg("The file '{key_path}' has been successfully uploaded to S3!"
            .format(key_path=key_path))
