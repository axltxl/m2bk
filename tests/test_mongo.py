"""
Test for: mongo
"""

from nose.tools import raises, eq_, ok_
from m2s3 import mongo
import os


@raises(TypeError)
def test_make_tarfile_nonstr():
    # _make_tarfile with non-string src_dir
    mongo._make_tarfile(123)


def test_make_tarfile():
    # whether the file name return is the expected
    out_dir = "../data"
    out_file = out_dir + '.tar.gz'
    eq_(mongo._make_tarfile(out_dir), out_file)
    # whether the expected file exists
    ok_(open(out_file))
    os.remove(out_file)


@raises(TypeError)
def test_make_backup_file_nondict():
    # make_backup_file with non-dict data
    mongo.make_backup_file(123)


@raises(TypeError)
def test_make_backup_file_invalid():
    # make_backup_file with invalid values within data
    # (for example, when type(data['mongodump']) == int)
    mongo.make_backup_file({'mongodump': 123})


@raises(ValueError)
def test_make_backup_file_empty_db():
    # with either invalid or empty dbs, it has to be an array in the first place
    mongo.make_backup_file({'db': []})

