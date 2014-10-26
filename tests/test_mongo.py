"""
Test for: mongo
"""

from nose.tools import assert_raises, raises, eq_, ok_
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


def test_make_backup_file_invalid_kwargs():
    # mongodump must be str
    assert_raises(TypeError, mongo.make_backup_file, mongodump=123)
    assert_raises(TypeError, mongo.make_backup_file, mongodump='')
    # output_dir must be str
    assert_raises(TypeError, mongo.make_backup_file, output_dir=123)
    assert_raises(TypeError, mongo.make_backup_file, output_dir='')
    # host must be str
    assert_raises(TypeError, mongo.make_backup_file, host=123)
    assert_raises(TypeError, mongo.make_backup_file, host='')
    # port must be int
    assert_raises(TypeError, mongo.make_backup_file, port="123")
    assert_raises(TypeError, mongo.make_backup_file, port='')
    # user_name must be str
    assert_raises(TypeError, mongo.make_backup_file, user_name=123)
    assert_raises(TypeError, mongo.make_backup_file, user_name='')
    # password must be str
    assert_raises(TypeError, mongo.make_backup_file, password=123)
    assert_raises(TypeError, mongo.make_backup_file, password='')


def test_make_backup_file_invalid_dbs():
    # with either invalid or empty dbs, it has to be an array in the first place
    assert_raises(ValueError, mongo.make_backup_file, dbs=[])
    assert_raises(ValueError, mongo.make_backup_file, dbs=123)
    assert_raises(TypeError, mongo.make_backup_file, dbs=['asd', 123])

