# -*- coding: utf-8 -*-

"""
m2bk.app
~~~~~~~~

Main module

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import os
import sys
import traceback
import argparse
import signal
from m2bk import config, log, mongo, s3, fs
from m2bk import __version__ as version
from m2bk.const import (
    LOG_LVL_DEFAULT,
    PKG_NAME, PKG_URL,
    CONF_DEFAULT_FILE
)

# command line options and flags
_opt = {}


def init_parsecmdline(argv=[]):
    """
    Parse arguments from the command line

    :param argv: list of arguments
    """
    # main argument parser
    parser = argparse.ArgumentParser(prog=PKG_NAME)

    # --version
    parser.add_argument('--version', action='version', version=version)

    # -c, --config <file_name>
    parser.add_argument("-c", "--config",
                  action="store",
                  dest="config_file", default=CONF_DEFAULT_FILE,
                  help="specify configuration file to use")

    # --dry-run
    parser.add_argument("-d", "--dry-run",
                   action="store_true",  dest="dry_run", default=False,
                   help="don't actually do anything")

    # --log-to-stdout
    parser.add_argument("-s", "--stdout",
                   action="store_true",  dest="log_to_stdout", default=False,
                   help="log also to stdout")

    # --ll <level>
    # logging level
    parser.add_argument("--ll", "--log-level",
                  action="store", type=int,
                  dest="log_lvl", default=LOG_LVL_DEFAULT,
                  help="set logging level")

    # Absorb the options
    options = parser.parse_args(argv)

    # Set whether we are going to perform a dry run
    global _opt
    _opt["dry_run"] = options.dry_run
    _opt["log_to_stdout"] = options.log_to_stdout
    _opt["log_lvl"] = options.log_lvl

    # Initiate the log level
    log.init(_opt['log_lvl'], _opt["log_to_stdout"])

    # Mark the start of executions
    log.msg("{pkg} [{version}] - {url}".format(pkg=PKG_NAME, version=version, url=PKG_URL))
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


def init(argv):
    """
    Bootstrap the whole thing

    :param argv: list of command line arguments
    """
    # Setting initial configuration values
    config.set_default({
        # fs section
        "fs": {},
        # Amazon Web Services section
        "aws": {},
        # MongoDB section
        "mongodb": {},
    })

    # Parse the command line
    init_parsecmdline(argv[1:])

    # Initiatize the output directory
    fs.init(**config.get_entry('fs'))

    # This baby will handle UNIX signals
    signal.signal(signal.SIGINT,  _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)


def _handle_signal(signum, frame):
    """
    UNIX signal handler
    """
    shutdown()


def shutdown():
    """
    Cleanup
    """
    fs.cleanup()
    log.msg("Exiting...")


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


def make_backup_files(mongodb, aws):

    #  dry run
    dry_run = _opt["dry_run"]

    # Generate a backup file from mongodump
    # This file should be compressed as a gzipped tarball
    mongodump_files = mongo.make_backup_files(dry_run=dry_run, **mongodb)

    # Upload the resulting file to AWS
    for key_name, file_name in mongodump_files.items():
        s3.upload_file(file_name, key_name, dry_run=dry_run, **aws)


def main(argv=None):
    """
    This is the main thread of execution

    :param argv: list of command line arguments
    """
    # Exit code
    exit_code = 0

    # First, we change main() to take an optional 'argv'
    # argument, which allows us to call it from the interactive
    # Python prompt
    if argv is None:
        argv = sys.argv

    try:
        # Bootstrap
        init(argv)

        #
        make_backup_files(config.get_entry('mongodb'), config.get_entry('aws'))

    except Exception as e:
        # ... and if everything else fails
        _handle_except(e)
        exit_code = 1
    finally:
        shutdown()
        return exit_code


# Now the sys.exit() calls are annoying: when main() calls
# sys.exit(), your interactive Python interpreter will exit!.
# The remedy is to let main()'s return value specify the
# exit status.
if __name__ == '__main__':
    sys.exit(main())



