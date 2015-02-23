#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) Alejandro Ricoveri
m2bk: A command line tool to simplify MongoDB backups

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---------------------------
setuptools config file
"""

from setuptools import setup, find_packages
import versioneer
import sys
import os
from m2bk.const import PKG_NAME

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

pkg_url = "https://github.com/axltxl/{p}".format(p=PKG_NAME)
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
    url=pkg_url,
    license='MIT',
    download_url="{url}/tarball/{version}".format(url=pkg_url, version=pkg_ver),
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