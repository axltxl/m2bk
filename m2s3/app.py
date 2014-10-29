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

# command line options and flags
_opt = {}

def init_parsecmdline(argv=[]):
    """
    Parse arguments from the command line

    :param argv: list of arguments
    """
    #https://docs.python.org/3.1/library/optparse.html#module-optparse
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage=usage, version=get_desc())

    # -c, --config <file_name>
    parser.add_option("-c", "--config",
                  action="store", type="string",
                  dest="config_file", default=CONF_DEFAULT_FILE,
                  help="specify configuration file to use")

    # --dry-run
    parser.add_option("-d", "--dry-run",
                   action="store_true",  dest="dry_run", default=False,
                   help="don't actually do anything")

    # --log-to-stdout
    parser.add_option("-s", "--stdout",
                   action="store_true",  dest="log_to_stdout", default=False,
                   help="log also to stdout")

    # --ll <level>
    parser.add_option("--ll", "--log-level",
                  action="store", type="int",
                  dest="log_lvl", default=LOG_LVL_DEFAULT,
                  help="set logging level")

    # Absorb the options
    (options, args) = parser.parse_args(argv)

    # Set whether we are going to perform a dry run
    global _opt
    _opt["dry_run"] = options.dry_run
    _opt["log_to_stdout"] = options.log_to_stdout
    _opt["log_lvl"] = options.log_lvl

    log.init(_opt['log_lvl'], _opt["log_to_stdout"])

    # Mark the start of executions
    log.msg('***************************************')

    # Merge configuration with a JSON file
    config_file = os.path.abspath(options.config_file)
    log.msg("Attempting to use configuration file '{config_file}'"
            .format(config_file=config_file))
    try:
        config.set_from_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file '{config_file}' not found!"
                                .format(config_file=config_file))


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

    :param argv: list of command line arguments
    """
    # Setting initial configuration values
    config.set_default({
        # Debug flag
        "debug": False,
        # Amazon Web Services section
        "aws": {},
        # MongoDB section
        "mongodb": {}
    })

    # Parse the command line
    init_parsecmdline(argv[1:])


def _handle_except(e):
    """
    Handle (log) any exception

    :param e: exception to be handled
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

    :param argv: list of command line arguments
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
            dry_run=_opt["dry_run"], **config.get_entry('mongodb')
        )
        # Upload the resulting file to AWS
        s3.upload_file(mongodump_filename,
            dry_run=_opt["dry_run"], **config.get_entry('aws')
        )
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



