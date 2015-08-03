# -*- coding: utf-8 -*-

"""
Test for: s3
"""

from nose.tools import assert_raises, eq_
from m2bk.drivers import s3

FILE = 'example.txt'

def test_upload_file_invalid_types():
    # Wrong ID
    assert_raises(TypeError, s3.load, aws_access_key_id=123)
    # Wrong access key
    assert_raises(TypeError, s3.load, aws_secret_access_key=True)
    # Wrong bucket name
    assert_raises(TypeError, s3.load,  s3_bucket=123)
    assert_raises(ValueError, s3.load, s3_bucket='')

def test_driver_init():
    s3.dispose()
    s3.load(dry_run=True)
    s3.backup_file(file="dummy.txt", host="dummy")
    eq_(True, s3._has_init)

    s3.dispose()
    assert_raises(RuntimeError, s3.backup_file, file="dummy.txt", host="dummy")
