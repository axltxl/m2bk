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
from ..const import PKG_NAME

#
# Constants
#
AWS_S3_DEFAULT_BUCKET_NAME = PKG_NAME

# Dry run mode
_dry_run = False

# Initialisation flag
_has_init = False

# AWS-specific options
_aws_access_key_id = None
_aws_secret_access_key = None
_bucket_name = None
_boto_conn = None


def load(*,
         aws_access_key_id=None,
         aws_secret_access_key=None,
         s3_bucket=AWS_S3_DEFAULT_BUCKET_NAME,
         dry_run=False,
         **kwargs):
    """
    Load this driver

    Note that if either aws_access_key_id or aws_secret_access_key are
    not specified, they will not be taken into account and instead
    authentication towards AWS will solely rely on boto config

    :param aws_access_key_id(str, optional): Access key ID
    :param aws_secret_access_key(str, optional): Secret access key
    :param s3_bucket(str, optional): Name of the S3 bucket to be used to store the file
    :param dry_run(bool, optional): Whether to activate dry run mode on this driver
    :param \*\*kwargs: arbitrary keyword arguments
    """
    global _dry_run, _has_init
    global _aws_access_key_id, _aws_secret_access_key, _bucket_name, _boto_conn

    # dry run
    _dry_run = dry_run

    # AWS parameters from kwargs
    _aws_access_key_id = aws_access_key_id
    _aws_secret_access_key = aws_secret_access_key
    if _aws_access_key_id is not None and type(_aws_access_key_id) != str:
        raise TypeError('aws_access_key_id must be str')
    if _aws_secret_access_key is not None \
       and type(_aws_secret_access_key) != str:
        raise TypeError('aws_secret_access_key must be str')

    # Check the bucket name before doing anything
    _bucket_name = s3_bucket
    if type(_bucket_name) != str:
        raise TypeError('s3_bucket must be str')
    if not _bucket_name:
        raise ValueError("s3_bucket cannot be empty")

    # Connect to S3 service
    log.msg("Connecting to Amazon S3 Service")
    if not _aws_access_key_id or not _aws_secret_access_key:
        log.msg_warn("No AWS credentials were given. " +
                     "Authentication will be done via boto.config/IAM role")
        if not _dry_run:
            _boto_conn = boto.connect_s3()
    elif not _dry_run:
        _boto_conn = boto.connect_s3(aws_access_key_id=_aws_access_key_id,
                                     aws_secret_access_key=_aws_secret_access_key)
    log.msg("Connected to AWS S3 service successfully!")

    # Indicate this driver has been properly initialised
    _has_init = True


def dispose():
    """
    Perform cleanup
    """
    global _has_init
    _has_init = False


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

    # This driver won't do a thing unless it has been properly initialised
    # via load()
    if not _has_init:
        raise RuntimeError("This driver has not been properly initialised!")

    # If the destination bucket does not exist, create one
    try:
        if not _dry_run:
            bucket = _boto_conn.get_bucket(_bucket_name)
    except boto.exception.S3ResponseError:
        log.msg_warn("Bucket '{bucket_name}' does not exist!, creating it..."
                     .format(bucket_name=_bucket_name))
        if not _dry_run:
            bucket = _boto_conn.create_bucket(_bucket_name)
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
