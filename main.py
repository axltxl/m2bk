#!/usr/bin/env python3
"""
Copyright (C) 2014 Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
Main module
"""

import sys
#import boto # Our nice AWS boto
import json
import os
import log
import config

def init_parseCmdLine ():
  """ """
  cmd_result = {} #
  argv = sys.argv #

  if len(argv[1:]) >= 1:
    cmd_result['config_file'] = argv[1]
  #
  return cmd_result

def init() :
  """ """

  #
  config.setDefault({
    "debug" : True,
    "log" : {
      "level" : -1
    },

    # Not needed if running from an instance 
    # with an IAM role
    "aws" : {
      "id" : "",
      "access_key" : ""
    },

    #
    "mongodb" : {
      "host" : "127.0.0.1",
      "port" : 27017,
      "user_name" : "mongo",
      "password"  : "pass",
      "dbs"   : [ "test" ]
    }
  })

  #
  log.msg ("Initiating ...")

  #
  cmd_result = init_parseCmdLine()
  if 'config_file' in cmd_result:
    config.setFromFile(cmd_result['config_file'])
  else:
    #
    config.setFromFile("/etc/m2s3.conf")

"""
"""
if __name__ == "__main__":
  try:

    #
    init()

    # 
    #aws.mongodump()
  #
  except Exception as e:
    log.msg_err (str(e))
    sys.exit(1)



