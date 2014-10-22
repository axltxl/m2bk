"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
setuptools config file
"""

from setuptools import setup, find_packages
import versioneer

# versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'm2s3/_version.py'
versioneer.versionfile_build = 'm2s3/_version.py'
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = 'm2s3-' # dirname like 'myproject-1.2.0'

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
    install_requires = ['boto >= 2.33.0'],
    author = "Alejandro Ricoveri",
    author_email = "alejandro.ricoveri@blanclink.com",
    description = "mongodump straight to Amazon S3",
    long_description = "m2s3 is able to perform mongodb backups via mongodump "
                       "and then send them straight to Amazon S3 buckets",
    #TODO set up default config install destination
    #data_files = ['data/m2s3.conf']
)