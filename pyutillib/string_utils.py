'''
pyutillib/string_utils.py

Copyright (C) 2013 Edwin van Opstal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see `<http://www.gnu.org/licenses/>`.
'''

from __future__ import division
from __future__ import absolute_import

import ast
import random
import string


def random_string(length=8, charset=None):
    '''
    Generates a string with random characters. If no charset is specified, only
    letters and digits are used.

    Args:
        length (int) length of the returned string
        charset (string) list of characters to choose from
    Returns:
        (str) with random characters from charset
    Raises:
        -
    '''
    if length < 1:
        raise ValueError('Length must be > 0')
    if not charset:
        charset = string.letters + string.digits
    return ''.join(random.choice(charset) for unused in xrange(length))


def safe_eval(str_in):
    '''
    Extracts a python object from a string.

    Args:
        str_in (string) that contains python variable
    Returns:
        (object) of standard python type or None of no valid object was found.
    Raises:
        -
    '''
    try:
        return ast.literal_eval(str_in)
    except:
        return None


def str2dict(str_in):
    '''
    Extracts a dict from a string.

    Args:
        str_in (string) that contains python dict
    Returns:
        (dict) or None if no valid dict was found
    Raises:
        -
    '''
    dict_out = safe_eval(str_in)
    if not isinstance(dict_out, dict):
        dict_out = None
    return dict_out


def str2tuple(str_in):
    '''
    Extracts a tuple from a string.

    Args:
        str_in (string) that contains python tuple
    Returns:
        (dict) or None if no valid tuple was found
    Raises:
        -
    '''
    tuple_out = safe_eval(str_in)
    if not isinstance(tuple_out, tuple):
        tuple_out = None
    return tuple_out


#used to be get_dict_keys
def str2dict_keys(str_in):
    '''
    Extracts the keys from a string that represents a dict and returns them
    sorted by key.

    Args:
        str_in (string) that contains python dict
    Returns:
        (list) with keys or None if no valid dict was found
    Raises:
        -
    '''
    tmp_dict = str2dict(str_in)
    if tmp_dict is None:
        return None
    return sorted([k for k in tmp_dict])


#used to be get_dict_values
def str2dict_values(str_in):
    '''
    Extracts the values from a string that represents a dict and returns them
    sorted by key.

    Args:
        str_in (string) that contains python dict
    Returns:
        (list) with values or None if no valid dict was found
    Raises:
        -
    '''
    tmp_dict = str2dict(str_in)
    if tmp_dict is None:
        return None
    return [tmp_dict[key] for key in sorted(k for k in tmp_dict)]
