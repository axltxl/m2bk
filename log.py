"""
Copyright (C) 2014 Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
Log messages module:
It basically handles local and systemwide logging into files.
Systemwide messages are logged through syslog.
"""

import config
import syslog

def msg (msg, lvl = 0):
  """ """
  #
  if lvl >= config.get('log')['level']:
    #
    syslog_prio = 0
    if lvl == -1:
      syslog_prio = syslog.LOG_DEBUG
    elif lvl == 0:
      syslog_prio = syslog.LOG_INFO
    elif lvl == 1:
      syslog_prio = syslog.LOG_WARNING
    elif lvl >= 2:
      syslog_prio = syslog.LOG_ERR

    # 
    syslog.syslog (syslog_prio, msg)

def msg_warn (message):
  """ """
  msg ( fmt('warn', message), 1 )

def msg_err (message):
  """ """
  msg ( fmt('error', message), 2 )

def msg_debug (message):
  """ """
  if config.get('debug') == True:
    msg ( fmt('debug', message),-1 )

def fmt (prefix, message):
  """ """
  return "[{prefix}] -- {msg}".format(prefix=prefix.upper(), msg=message)