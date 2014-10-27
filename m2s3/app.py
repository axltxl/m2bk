"""
Copyright (C) Blanclink, Inc.
---------------------------
m2s3: A mongodump straight to AWS-S3
Author: Alejandro Ricoveri <alejandro.ricoveri@blanclink.com>
---------------------------
Main module
"""

import os
import sys
import traceback
#TODO replace log with logging https://docs.python.org/3.4/howto/logging.html#logging-basic-tutorial
from m2s3 import config, log, mongo, s3
from m2s3 import __version__ as version
from optparse import OptionParser
from m2s3.const import (
    LOG_LVL_DEFAULT,
    PKG_NAME,
    CONF_DEFAULT_FILE
)


def init_parsecmdline(argv=[]):
    """
    Parse arguments from the command line
    """
    #https://docs.python.org/3.1/library/optparse.html#module-optparse
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage=usage, version=get_desc())

    # -c, --config <file_name>
    parser.add_option("-c", "--config",
                  action="store", type="string",
                  dest="config_file", default=CONF_DEFAULT_FILE,
                  help="specify configuration file to use")

    # --dry-run (to be implemented)
    # parser.add_option("-d", "--dry-run",
    #               action="store_true",  dest="dry_run", default=False,
    #               help="don’t actually perform the actions, "
    #                    "just show whether it is possible to do them and how")

    # Absorb the options
    (options, args) = parser.parse_args(argv)

    # Merge configuration with a JSON file
    config_file = os.path.abspath(options.config_file)
    log.msg("Attempting to use configuration file '{config_file}'"
            .format(config_file=config_file))
    try:
        config.set_from_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file not found!")

    # Set whether we are going to perform a dry run
    #config.set_entry('dry_run', options.dry_run)


def get_desc():
    """
    Description string

    :return: a string with the package name and its version
    """
    return "{pkg_name} {pkg_version}"\
        .format(pkg_name=PKG_NAME, pkg_version=version)

def init(argv):
    """
    Bootstrap the whole thing
    """
    # Setting initial configuration values
    config.set_default({
        "debug": True,
        "log": {
            "level": LOG_LVL_DEFAULT
        },
        # Not needed if running from an instance
        # with an IAM role
        "aws": {},
        # MongoDB
        "mongodb": {}
    })

    # Mark the start of executions
    log.msg('***************************************')

    # Parse the command line
    init_parsecmdline(argv[1:])

    # Configure log module
    log.threshold = config.get_entry('log')['level']
    log.debug = config.get_entry('debug')


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
        # Get the thing done
        mongodump_filename = mongo.make_backup_file(**config.get_entry('mongodb'))
        # Upload the resulting file to AWS
        s3.upload_file(mongodump_filename, **config.get_entry('aws'))
    #TODO better exception handling
    except Exception as e:
        # ... and if everything else fails
        log.msg_err(traceback.format_exc())
        return 1

# Now the sys.exit() calls are annoying: when main() calls
# sys.exit(), your interactive Python interpreter will exit!.
# The remedy is to let main()'s return value specify the
# exit status.
if __name__ == '__main__':
    sys.exit(main())



