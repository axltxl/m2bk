# -*- coding: utf-8 -*-

"""
m2bk.utils
~~~~~~~~~~

Utilities

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""


def chkstr(s, v):
    """
    Small routine for checking whether a string is empty
    even a string

    :param s: the string in question
    :param v: variable name
    """
    if type(s) != str:
        raise TypeError("{var} must be str".format(var=v))
    if not s:
        raise ValueError("{var} cannot be empty".format(var=v))