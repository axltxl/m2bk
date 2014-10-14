"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
Main module
"""

import sys
#TODO replace log with logging https://docs.python.org/3.4/howto/logging.html#logging-basic-tutorial
from m2s3 import config, log, mongo


def init_parsecmdline(argv):
    """
    Parse arguments from the command line
    """
    #TODO replace this with optparse https://docs.python.org/3.1/library/optparse.html#module-optparse
    argv_result = {}
    if len(argv[1:]) >= 1:
        argv_result['config_file'] = argv[1]
    return argv_result


def init(argv):
    """
    Bootstrap the whole thing
    """
    # Setting initial configuration values
    config.set_default({
        "debug": True,
        "log": {
            "level": -1
        },
        # Not needed if running from an instance
        # with an IAM role
        "aws": {
            "id": "",
            "access_key": ""
        },
        # MongoDB
        "mongodb": {
            "host": "127.0.0.1",
            "port": 27017,
            "user_name": "mongo",
            "password": "pass",
            "dbs": ["test"]
        }
    })

    # Merge configuration with a JSON file
    cmd_result = init_parsecmdline(argv)
    if 'config_file' in cmd_result:
        config.set_from_file(cmd_result['config_file'])
    else:
        config.set_from_file("/etc/m2s3.conf")

    # Configure log module
    log.threshold = config.get_entry('log')['level']
    log.debug = config.get_entry('debug')
    log.msg("Initiating ...")


def main(argv=None):
    """
    This is the main thread of execution
    """

    # First, we change main() to take an optional 'argv'
    # argument, which allows us to call it from the interactive
    # Python prompt
    if argv is None:
        argv = sys.argv

    try:
        # Bootstrap
        init(argv)
        #TODO design and implement mongodump phase for each db
        #TODO design and implement s3 phase for each mongodump
        # aws.mongodump()
        mongo.fetch(config.get_entry('mongodb'))
    # ... and if everything else fails
    #TODO better exception handling
    except Exception as e:
        log.msg_err(str(e))
        return 1

# Now the sys.exit() calls are annoying: when main() calls
# sys.exit(), your interactive Python interpreter will exit!.
# The remedy is to let main()'s return value specify the
# exit status.
if __name__ == '__main__':
    sys.exit(main())



