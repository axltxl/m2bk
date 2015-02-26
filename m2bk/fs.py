# -*- coding: utf-8 -*-

"""
m2bk.fs
~~~~~~~

File system management

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import os
import tarfile
import stat
import shutil
from . import utils, log
from .const import FS_DEFAULT_OUTPUT_DIR

# Output directory name
_output_dir = None


def get_output_dir():
    """
    Get the name of the output directory

    :return: a str containing the output directory
    """
    return _output_dir


def init(**kwargs):
    """
    Set up output directory

    :param \*\*kwargs: arbitrary keyword arguments
    :return:
    """
    # Output directory
    global _output_dir
    _output_dir = kwargs.get('output_dir', FS_DEFAULT_OUTPUT_DIR)

    # Type checks
    utils.chkstr(_output_dir, 'output_dir')

    # log the thing
    log.msg("Output directory will be: {output_dir}".format(output_dir=_output_dir))

    # Create output directory if it does not exist
    if not os.path.exists(_output_dir):
        log.msg_warn("Output path '{output_dir}' does not exist, creating it ...".format(output_dir=_output_dir))
        # create the actual root output directory
        os.makedirs(_output_dir)
        # set folder permissions to 0770
        os.chmod(_output_dir, stat.S_IRWXU | stat.S_IRWXG)


def cleanup():
    """
    Cleanup the output directory
    """
    if _output_dir and os.path.exists(_output_dir):
        log.msg_warn("Cleaning up output directory at '{output_dir}' ...".format(output_dir=_output_dir))
        shutil.rmtree(_output_dir)


def make_file(src_dir):
    """
    Make gzipped tarball from a source directory

    :param src_dir: source directory
    :raises TypeError: if src_dir is not str
    """
    if type(src_dir) != str:
        raise TypeError('src_dir must be str')
    output_file = src_dir + ".tar.gz"
    log.msg("Wrapping tarball '{out}' ...".format(out=output_file))
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(src_dir, arcname=os.path.basename(src_dir))
    return output_file