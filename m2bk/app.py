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
from m2bk import config, log, mongo, fs
from m2bk import __version__ as version
from m2bk.const import (
    PKG_NAME, PKG_URL
)
from m2bk import driver
from m2bk.utils import debug

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
                        dest="config_file", default=config.CONF_DEFAULT_FILE,
                        help="specify configuration file to use")

    # --dry-run
    parser.add_argument("-d", "--dry-run",
                        action="store_true",  dest="dry_run", default=False,
                        help="don't actually do anything")

    # --quiet
    parser.add_argument("-q", "--quiet",
                        action="store_true",  dest="log_quiet", default=False,
                        help="quiet output")

    # --ll <level>
    # logging level
    parser.add_argument("--ll", "--log-level",
                        action="store", type=int,
                        dest="log_lvl", default=log.LOG_LVL_DEFAULT,
                        help="set logging level")

    # -l, --log-file
    parser.add_argument("-l", "--log-file",
                        action="store",
                        dest="log_file", default=log.LOG_FILE_DEFAULT,
                        help="set log file")

    # Absorb the options
    options = parser.parse_args(argv)

    # Set whether we are going to perform a dry run
    global _opt
    _opt["dry_run"] = options.dry_run

    # Initiate the log level
    log.init(threshold_lvl=options.log_lvl,
             quiet_stdout=options.log_quiet, log_file=options.log_file)

    #
    # Print the splash
    #
    _splash()

    # Merge configuration with a JSON file
    config_file = os.path.abspath(options.config_file)
    log.msg("Attempting to use configuration file '{config_file}'"
            .format(config_file=config_file))
    try:
        config.set_from_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file '{config_file}' not found!"
                                .format(config_file=config_file))


def _splash():
    """Print the splash"""
    splash_title = "{pkg} [{version}] - {url}".format(pkg=PKG_NAME,
                                                      version=version, url=PKG_URL)
    log.to_stdout(splash_title, colorf=log.yellow, bold=True)
    log.to_stdout('-' * len(splash_title), colorf=log.yellow, bold=True)


def init(argv):
    """
    Bootstrap the whole thing

    :param argv: list of command line arguments
    """
    # Setting initial configuration values
    config.set_default({
        # driver section
        "driver": {},
        # fs section
        "fs": {},
        # MongoDB section
        "mongodb": {},
    })

    # Parse the command line
    init_parsecmdline(argv[1:])

    # Initiatize the output directory
    fs.init(dry_run=_opt["dry_run"], **config.get_entry('fs'))

    # This baby will handle UNIX signals
    signal.signal(signal.SIGINT,  _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)


def _handle_signal(signum, frame):
    """
    UNIX signal handler
    """
    # Raise a SystemExit exception
    sys.exit(1)


def shutdown():
    """
    Cleanup
    """
    # TODO: driver.abort()
    driver.dispose()
    fs.cleanup()
    log.msg("Exiting ...")


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


def make_backup_files():

    #  dry run
    dry_run = _opt["dry_run"]

    # Load the driver before attempting anything
    driver.load(dry_run=dry_run, **config.get_entry('driver'))

    # Generate a backup file from mongodump
    # This file should be compressed as a gzipped tarball
    mongodump_files = mongo.make_backup_files(dry_run=dry_run,
                                              **config.get_entry('mongodb'))

    # Transfer the backup using a driver
    for host_name, file_name in mongodump_files.items():
        driver.backup_file(file=file_name, host=host_name)


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

        # Perform the actual backup job
        make_backup_files()

    except Exception as e:
        # ... and if everything else fails
        _handle_except(e)
        exit_code = 1
    finally:
        # All cleanup actions are taken from here
        shutdown()
        return exit_code


# Now the sys.exit() calls are annoying: when main() calls
# sys.exit(), your interactive Python interpreter will exit!.
# The remedy is to let main()'s return value specify the
# exit status.
if __name__ == '__main__':
    sys.exit(main())
