# -*- coding: utf-8 -*-

"""
Test for: fs
"""


from nose.tools import raises , ok_, assert_raises
import os
from m2bk import fs


@raises(TypeError)
def test_make_tarball_nonstr():
    # _make_tarfile with non-string src_dir
    fs.make_tarball(123)


def test_make_tarball():
    # whether the file name return is the expected
    out_dir = "data"
    out_file = out_dir + ".tar.gz"
    #eq_(mongo._make_tarfile(out_dir), out_file)
    # whether the expected file exists
    fs.make_tarball(out_dir)
    ok_(open(out_file), msg="Could not open expected output file")
    os.remove(out_file)


def test_init_invalid_kwargs():
    # output_dir must be str
    assert_raises(TypeError, fs.init, output_dir=123)
    assert_raises(ValueError, fs.init, output_dir='')