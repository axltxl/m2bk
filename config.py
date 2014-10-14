"""
Copyright (C) 2014 Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
{desc}
"""

import log
import json

#
_config = {}


def get (key) :
  """ """
  if key in _config:
    return _config[key]
  return 0 # temp


def set (key, value):
  """ """
  _config[key] = value


def setDefault (cfg):
  """ """
  global _config
  _config = cfg


def setFromFile (file_name):
    """ """

  #
  try:

    #
    log.msg_debug ("Current configuration file: {cfg}".format(cfg=file_name))

    #
    with open (file_name, "r") as file:
      data = json.loads( file.read().replace('\n', '') )

    #
    for k in data:
      _config[k] = data[k]

  except Exception as e:
    #
    log.msg_err ("Unable to open configuration file: {fn}".format(fn=file_name))
    log.msg_err ("Reason: {r}".format(r=str(e)))
    log.msg ('Omitting configuration file ...')
