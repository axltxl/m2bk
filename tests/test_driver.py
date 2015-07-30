# -*- coding: utf-8 -*-

"""
Test for: backup drivers
"""

from nose.tools import raises, eq_, ok_, assert_raises
from m2bk import driver

#
# Test dummy driver
#

def test_driver_selection():
    for d in ['dummy', 's3']:
        driver.load(name=d, dry_run=True)
        eq_(d, driver.get_name())
        driver.dispose()
    # test invalid driver
    assert_raises(ValueError, driver.load, name="idonotexist")
