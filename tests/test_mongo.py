"""
Test for: mongo
"""

from nose.tools import assert_equals
from m2s3 import app, config, const

def test_make_tarfile():
    # _make_tarfile with invalid directory
    # _make_tarfile with non-string src_dir
    pass


def make_backup_file():
    # make_backup_file with valid data
    # make_backup_file with non-dict data
    # make_backup_file with invalid values within data
    # (for example, when type(data['mongodump']) == int)
    # with either empty user_name or password
    # with either invalid or empty dbs, it has to be an array in the first place
    pass

def test_mongodump():
    pass
