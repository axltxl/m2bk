"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
Constants
"""

# Basics
PKG_NAME = "m2s3"

# Logs
LOG_LVL_DEFAULT = -1

# Amazon S3
AWS_DEFAULT_ID = ""
AWS_DEFAULT_ACCESS_KEY = ""
AWS_S3_DEFAULT_BUCKET_NAME = PKG_NAME

# Config
CONF_DEFAULT_FILE = "/etc/{pkg_name}.conf".format(pkg_name=PKG_NAME)

# mongodump
MONGODB_DEFAULT_MONGODUMP = "mongodump"
MONGODB_DEFAULT_OUTPUT_DIR = "/tmp/{pkg_name}".format(pkg_name=PKG_NAME)
MONGODB_DEFAULT_USER = PKG_NAME
MONGODB_DEFAULT_PWD = "pass"
MONGODB_DEFAULT_HOST = "localhost"
MONGODB_DEFAULT_PORT = 27017
