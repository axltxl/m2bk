"""
Copyright (c) Alejandro Ricoveri
m2s3: A mongodump straight to AWS S3

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

# versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'm2s3/_version.py'
versioneer.versionfile_build = 'm2s3/_version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = 'm2s3-'

# default config file location
if sys.prefix != '/usr':
    conf_dir = os.path.join(sys.prefix, 'etc')
else:
    conf_dir = '/etc'

setup(
    name = "m2s3",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages = find_packages(exclude=["tests"]),
    entry_points={
        'console_scripts': [
            'm2s3 = m2s3.app:main',
        ],
    },
    install_requires = [
        'boto==2.34.0'
    ],
    tests_require = [
        'nose>=1.3'
    ],
    author = "Alejandro Ricoveri",
    author_email = "alejandro.ricoveri@blanclink.com",
    description = "mongodump straight to Amazon S3",
    long_description = "m2s3 is able to perform mongodb backups via mongodump "
                       "and then send them straight to Amazon S3 buckets",
    test_suite="nose.collector",
    data_files = [
        (conf_dir, ['data/m2s3.conf'])
    ]
)