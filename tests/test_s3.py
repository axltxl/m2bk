"""
Test for: s3
"""

from nose.tools import eq_, ok_, raises
from m2s3 import s3, config

def setup():
    config.clear()

@raises(TypeError)
def test_backup_file_nonstr():
    s3.backup_file(123)

@raises(ValueError)
def test_backup_file_incomplete_aws():
    config.set_entry('aws', {'id' : 123})
    s3.backup_file('file.txt')