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
Constants
"""

# Basics
PKG_NAME = "m2bk"
PKG_URL  = "https://github.com/axltxl/{pkg_name}".format(pkg_name=PKG_NAME)

# Logs
LOG_LVL_DEFAULT = 0

# Amazon S3
AWS_DEFAULT_ID = ""
AWS_DEFAULT_ACCESS_KEY = ""
AWS_S3_DEFAULT_BUCKET_NAME = PKG_NAME

# Config
CONF_DEFAULT_FILE = "/etc/{pkg_name}.yaml".format(pkg_name=PKG_NAME)

# mongodump
MONGODB_DEFAULT_MONGODUMP = "mongodump"
MONGODB_DEFAULT_USER = PKG_NAME
MONGODB_DEFAULT_PWD = "pass"
MONGODB_DEFAULT_PORT = 27017

#fs
FS_DEFAULT_OUTPUT_DIR = "/tmp/{pkg_name}".format(pkg_name=PKG_NAME)
