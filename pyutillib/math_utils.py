'''
pyutillib/math_utils.py

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

import operator
from pyutillib.string_utils import str2tuple


def div(numerator, denominator):
    '''
    Returns numerator / denominator, but instead of a ZeroDivisionError:
        0 / 0 = 0.
        x / 0 = float('inf')
    This is not mathematically correct, but often practically OK.

    Args:
        numerator (float or int)
        denominator (float or int)
    Returns:
        (float)
    Raises:
        -
    '''
    try:
        return numerator/denominator
    except ZeroDivisionError:
        if numerator == 0:
            return 0.
        elif denominator == 0:
            return float('inf')
#            return None
        else:
            return numerator/denominator


def eval_conditions(conditions=None, data={}):
    '''
    Evaluates conditions and returns Boolean value.

    Args:
        conditions (tuple) for the format of the tuple, see below
        data (dict) the keys of which can be used in conditions
    Returns:
        (boolea)
    Raises:
        ValueError if an invalid operator value is specified
        TypeError if: 
                conditions are not a 3-item tuple
                the arguments of the condition don't have the same type
                    e.g. ('abc', 'eq', 3)
                if a boolean operator does not get boolean arguments
                    e.g. (True, 'and', 15)

    The format of the condition tuple is:
        (arg1, op, arg2)
    where:
        arg1, arg2 can be numerical values, strings or condition tuples
        op is a valid operator from the operator module
    If arg is a string, and the string is a key in <data> it is treated as
    a variable with value data[arg].

    Notes:
        * If no conditions are specified True is returned.
        * empty or 0 values do *not* evaluate to booleans
    '''
#CONSIDER: implementing addition/subtraction/multiplication/division
    if not conditions:
        return True
    if isinstance(conditions, str) or isinstance(conditions, unicode):
        conditions = str2tuple(conditions)
    if not isinstance(conditions, tuple) or not len(conditions) == 3:
        raise TypeError('conditions must be a tuple with 3 items.')
    arg1 = conditions[0]
    op = conditions[1]
    arg2 = conditions[2]
    if arg1 in data:
        arg1 = data[arg1]
    elif isinstance(arg1, tuple):
        arg1 = eval_conditions(arg1, data)
    if arg2 in data:
        arg2 = data[arg2]
    elif isinstance(arg2, tuple):
        arg2 = eval_conditions(arg2, data)
    if op in ('lt', 'le', 'eq', 'ne', 'ge', 'gt'):
        if not (type(arg1) in (float, int) and type(arg2) in (float,int)) and \
                type(arg1) != type(arg2):
            raise TypeError('both arguments must have the same type {}, {}'.\
                    format(arg1, arg2))
    elif op in ('and', 'or'):
        if not isinstance(arg1, bool) or not isinstance(arg2, bool):
            raise TypeError('boolean operator {} needs boolean arguments {},'\
                    ' {}'.format(op, arg1, arg2))
        op += '_'
    else:
        raise ValueError('operator {} not supported', op)
    return getattr(operator, op)(arg1, arg2)
