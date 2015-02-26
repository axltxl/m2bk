# -*- coding: utf-8 -*-

"""
m2bk.s3
~~~~~~~

Backup files generated by mongodump on a S3 bucket

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import boto
import ntpath
from . import log
from .const import (
    AWS_DEFAULT_ACCESS_KEY,
    AWS_DEFAULT_ID,
    AWS_S3_DEFAULT_BUCKET_NAME
)


def upload_file(file_name, key_name, **kwargs):
    """
    Backup a file on S3

    :param file_name: full path to the file to be backed up
    :param key_name: this will be used to locate the file on S3
    :param \*\*kwargs: arbitrary keyword arguments
    :raises TypeError: if an argument in kwargs does not have the type expected
    :raises ValueError: if an argument within kwargs has an invalid value
    """

    # AWS parameters from kwargs
    aws_id = kwargs.get('aws_id', AWS_DEFAULT_ID)
    aws_key = kwargs.get('aws_access_key', AWS_DEFAULT_ACCESS_KEY)
    if type(aws_id) != str:
        raise TypeError('aws_id must be str')
    if type(aws_key) != str:
        raise TypeError('aws_access_key must be str')
    #dry run
    dry_run = kwargs.get('dry_run', False)
    # Check the bucket name before doing anything
    bucket_name = kwargs.get('s3_bucket', AWS_S3_DEFAULT_BUCKET_NAME)
    if type(bucket_name) != str:
        raise TypeError('s3_bucket must be str')
    if not bucket_name:
        raise ValueError("s3_bucket cannot be empty")

    # Connect to S3 service
    log.msg("Connecting to Amazon S3 Service")
    if not aws_id and not aws_key:
        log.msg_warn('No AWS credentials given. Assuming access via IAM role')
        if not dry_run:
            conn = boto.connect_s3()
    elif not aws_id or not aws_key:
        if aws_id:
            raise ValueError("aws_id given with no aws_access_key")
        else:
            raise ValueError("aws_access_key given with no aws_id")
    elif not dry_run:
        conn = boto.connect_s3(aws_access_key_id=aws_id,
                               aws_secret_access_key=aws_key)
    log.msg("Connected to AWS S3 service successfully!")
    # If the destination bucket does not exist, create one
    try:
        if not dry_run:
            bucket = conn.get_bucket(bucket_name)
    except boto.exception.S3ResponseError:
        log.msg_warn("Bucket '{bucket_name}' does not exist!, creating it..."
                     .format(bucket_name=bucket_name))
        if not dry_run:
            bucket = conn.create_bucket(bucket_name)
        log.msg("Created bucket '{bucket}'".format(bucket=bucket_name))

    # The key is the name of the file itself who needs to be stripped
    # from its full path
    key_path = "{key}/{file}".format(key=key_name, file=ntpath.basename(file_name))

    if not dry_run:
        # Create a new bucket key
        k = boto.s3.key.Key(bucket)
        k.key = key_path
    # Upload the file to Amazon
    log.msg("Uploading '{key_path}' to bucket '{bucket_name}' ..."
            .format(key_path=key_path, bucket_name=bucket_name))
    if not dry_run:
        # It is important to encrypt the data on the server side
        k.set_contents_from_filename(file_name, encrypt_key=True)
    log.msg("The file '{key_path}' has been successfully uploaded to S3!"
            .format(key_path=key_path))
