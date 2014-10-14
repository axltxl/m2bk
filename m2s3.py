#!/usr/bin/env python3
"""
Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
{description}
"""

import sys
#import boto # Our nice AWS boto
import json
import os
import syslog

def log (msg, lvl = 0):
  """ """

  #
  if lvl >= config['log']['level']:
    #
    syslog_prio = 0
    if lvl == -1:
      syslog_prio = syslog.LOG_DEBUG
    elif lvl == 0:
      syslog_prio = syslog.LOG_INFO
    elif lvl == 1:
      syslog_prio = syslog.LOG_WARNING
    elif lvl == 2:
      syslog_prio = syslog.LOG_ERR

    # 
    syslog.syslog (syslog_prio, msg)

    #
    if config["debug"] == True:
      print ("* {msg}".format(msg=msg))

def log_warning (msg):
  """ """
  log ("[WARN] -- {msg}".format(msg=msg), 1)

def log_error (msg):
  """ """
  log ("[ERROR] -- {msg}".format(msg=msg), 2)

def log_debug (msg):
  """ """
  if config["debug"] == True:
    log ("[DEBUG] -- {msg}".format(msg=msg), -1)

def parse_cmd_line (argv):
  """ """
  cmd_result = {}
  #global config_file
  if len(argv[1:]) >= 1:
    cmd_result['config_file'] = argv[1]

  #
  return cmd_result

def get_default_config ():
  """ """
  return {
    "debug" : True,
    "log" : {
      "level" : -1
    },

    # Not needed if running from an instance 
    # with an IAM role
    "aws" : {
      "id" : "<secret>",
      "access_key" : ""
    }
  }

def get_config (file_name):
  """ """

  #
  new_config = get_default_config()

  #
  try:

    # 
    with open (file_name, "r") as file:
      data = json.loads( file.read().replace('\n', '') )

    # 
    for k in data:
      new_config[k] = data[k]

  except Exception as e:
    log_error("Unable to open configuration file: {fn}"\
      .format(fn=file_name))
    log_error("Reason: {r}".format(r=str(e)))

  #
  log_debug ("Current configuration file: {cfg}".format(cfg=file_name))
  return new_config

"""
"""
try:

  # 
  config_file = "/etc/m2s3.conf"
  config      = get_default_config()

  #
  cmd_result = parse_cmd_line(sys.argv)
  if 'config_file' in cmd_result:
    config_file = cmd_result['config_file']

  #
  config = get_config(config_file)

  #
  show_config = config
  del show_config["aws"] # We cannot show AWS-related info in the logs
  log_debug ("Current configuration: {cfg}".format(cfg=config))
# 
except Exception as e:
  log_error (str(e))
  sys.exit(1)



