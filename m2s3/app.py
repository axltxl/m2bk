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
    #               help="don't actually do anything")

    # Absorb the options
    (options, args) = parser.parse_args(argv)

    # Merge configuration with a JSON file
    config_file = os.path.abspath(options.config_file)
    log.msg("Attempting to use configuration file '{config_file}'"
            .format(config_file=config_file))
    try:
        config.set_from_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file '{config_file}' not found!"
                                .format(config_file=config_file))

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
        # Debug flag
        "debug": True,
        # Logging section
        "log": {
            "level": LOG_LVL_DEFAULT
        },
        # Amazon Web Services section
        "aws": {},
        # MongoDB section
        "mongodb": {}
    })

    # Mark the start of executions
    log.msg('***************************************')

    # Parse the command line
    init_parsecmdline(argv[1:])

    # Configure log module
    log.threshold = config.get_entry('log')['level']
    log.debug = config.get_entry('debug')


def _handle_except(e):
    """
    Handle (log) any exception

    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.msg_err("Unhandled {e} at {file}:{line}: '{msg}'"
                .format(e=exc_type.__name__, file=fname,
                        line=exc_tb.tb_lineno,  msg=e))
    log.msg_err(traceback.format_exc())
    log.msg_err("An error has occurred!. "
                "For more details, review the logs.")
    return 1

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
        # Generate a backup file from mongodump
        # This file should be compressed as a gzipped tarball
        mongodump_filename = mongo.make_backup_file(
            **config.get_entry('mongodb')
        )
        # Upload the resulting file to AWS
        s3.upload_file(mongodump_filename, **config.get_entry('aws'))
    except Exception as e:
        # ... and if everything else fails
        return _handle_except(e)
    finally:
        log.msg("Exiting...")

# Now the sys.exit() calls are annoying: when main() calls
# sys.exit(), your interactive Python interpreter will exit!.
# The remedy is to let main()'s return value specify the
# exit status.
if __name__ == '__main__':
    sys.exit(main())



