# -*- coding: utf-8 -*-

"""
m2bk.const
~~~~~~~~~~

Constants

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

# Basics
PKG_NAME = "m2bk"
PKG_URL  = "https://github.com/axltxl/{pkg_name}".format(pkg_name=PKG_NAME)

# Logs
LOG_LVL_DEFAULT = 1

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
MONGODB_DEFAULT_AUTH = "admin"

#fs
FS_DEFAULT_OUTPUT_DIR = "/tmp/{pkg_name}".format(pkg_name=PKG_NAME)
