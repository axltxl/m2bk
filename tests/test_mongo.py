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
    out_dir = "data"
    out_file = out_dir + '.tar.gz'
    eq_(mongo._make_tarfile(out_dir), out_file)
    # whether the expected file exists
    ok_(open(out_file), msg="Could not open expected output file")
    os.remove(out_file)


def test_set_mongodb_host_val():
    """
    Test whether mongo._set_mongodb_host_val works well
    """
    last_resort = "mate"
    defaults = {
        'hello': 'world',
        'marco': 'polo'
    }
    values = {
        'marco': 'what?'
    }
    mongo._set_mongodb_host_val('marco', 'not_good', values, defaults)
    eq_(values['marco'], 'what?')

    mongo._set_mongodb_host_val('hello', 'not_good', values, defaults)
    eq_(values['hello'], 'world')

    mongo._set_mongodb_host_val('ello', last_resort, values, defaults)
    eq_(values['ello'], last_resort)


def _test_make_backup_files(e, **kwargs):
    """
    Individual test for mongo.make_backup_files
    """
    hosts = [
        {
            'name': 'ello',
            'address' : 'somehost',
            'dbs': ['marco', 'polo']
        },
        {
            'name': 'ello_again',
            'address': 'somehost',
            'dbs': ['marco', 'polo']
        }
    ]
    assert_raises(e, mongo.make_backup_files, dry_run=True, hosts=hosts, **kwargs)


def test_merge_dbs():
    a = ['hello', 'konichiwa']
    b = ['salam', 'hello', 'bonjour']
    # a + b = c (it should be)
    c = ['hello', 'salam', 'bonjour', 'konichiwa']
    eq_(sorted(c), sorted(mongo._merge_dbs(a,b)))

def test_make_backup_files_invalid_kwargs():
    """
    Several tests for mongo.make_backup_files
    """
    # hosts must be a list
    assert_raises(TypeError, mongo.make_backup_files, hosts=123)
    assert_raises(ValueError, mongo.make_backup_files, hosts=[])
    # mongodump must be str
    _test_make_backup_files(TypeError, mongodump=123)
    _test_make_backup_files(ValueError, mongodump='')
    # output_dir must be str
    _test_make_backup_files(TypeError, output_dir=123)
    _test_make_backup_files(ValueError, output_dir='')
    # port must be int
    _test_make_backup_files(TypeError, host_defaults={"port": "123"})
    # port must be between 1 and 65535
    _test_make_backup_files(ValueError, host_defaults={"port": -40})
    _test_make_backup_files(ValueError, host_defaults={"port": 340535})
    # user_name must be str
    _test_make_backup_files(TypeError, host_defaults={"user_name": 123})
    _test_make_backup_files(ValueError, host_defaults={"user_name": ''})
    # password must be str
    _test_make_backup_files(TypeError, host_defaults={"password": 123})
    _test_make_backup_files(ValueError, host_defaults={"password": ''})
    # name must be str
    assert_raises(TypeError, mongo.make_backup_files, hosts=[{'name': 123}])
    assert_raises(ValueError, mongo.make_backup_files, hosts=[{'name': ''}])

    # with either invalid or empty dbs, it has to be an array in the first place
    hosts = [
        {
            'name': 'ello',
            'address' : 'somehost',
            'dbs': []
        },
    ]
    assert_raises(ValueError, mongo.make_backup_files, hosts=hosts)

    hosts[0]["dbs"] = 123
    assert_raises(ValueError, mongo.make_backup_files, hosts=hosts)


    hosts[0]["dbs"] = ['asd', 123]
    assert_raises(TypeError, mongo.make_backup_files, hosts=hosts)

