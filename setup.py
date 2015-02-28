#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools config file
"""

import sys

# Check minimum Python version
PYVER_MAJOR = 3
PYVER_MINOR = 3
if not (sys.version_info[0] == PYVER_MAJOR and sys.version_info[1] >= PYVER_MINOR):
    print("Sorry, Python >= 3.3 is supported (for the moment")
    sys.exit(1)

from setuptools import setup, find_packages
import versioneer
import os
from m2bk.const import PKG_NAME, PKG_URL


# versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = "{p}/_version.py".format(p=PKG_NAME)
versioneer.versionfile_build = "{p}/_version.py".format(p=PKG_NAME)
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = "{p}-".format(p=PKG_NAME)

# default config file location
if sys.prefix != '/usr':
    conf_dir = os.path.join(sys.prefix, 'etc')
else:
    conf_dir = '/etc'

pkg_ver = versioneer.get_version()

setup(
    name=PKG_NAME,
    version=pkg_ver,
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["tests"]),
    author="Alejandro Ricoveri",
    author_email="alejandroricoveri@gmail.com",
    description="A command line tool to simplify MongoDB backups",
    long_description=open('README.rst').read(),
    url=PKG_URL,
    license='MIT',
    download_url="{url}/tarball/{version}".format(url=PKG_URL, version=pkg_ver),
    keywords=['mongodb', 'aws', 'backup', 's3'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console	',
        'Topic :: Database',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'm2bk = m2bk.app:main',
        ],
    },
    install_requires = [
        'boto  == 2.34.0',
        'envoy >= 0.0.3',
        'pyyaml >= 3.11',
    ],
    tests_require = ['nose >= 1.3'],
    test_suite="nose.collector",
    data_files=[(conf_dir, ['data/m2bk.yaml'])]
)