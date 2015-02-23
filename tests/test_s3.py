# -*- coding: utf-8 -*-

"""
Test for: s3
"""

from nose.tools import assert_raises
from m2bk import s3

FILE = 'example.txt'


def test_upload_file_incomplete_aws_credentials():
    # Raises Value error if either id or access_key are not present
    assert_raises(ValueError, s3.upload_file, FILE, 'testkey', aws_id='123456')
    assert_raises(ValueError, s3.upload_file, FILE, 'testkey', aws_access_key='asd')


def test_upload_file_invalid_types():
    # Wrong ID
    assert_raises(TypeError, s3.upload_file, FILE, 'testkey', aws_id=123)
    # Wrong access key
    assert_raises(TypeError, s3.upload_file, FILE, 'testkey', aws_access_key=True)
    # Wrong bucket name
    assert_raises(TypeError, s3.upload_file, FILE, 'testkey', s3_bucket=123)
    assert_raises(ValueError, s3.upload_file, FILE, 'testkey',s3_bucket='')