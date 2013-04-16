==================================================
pyutillib - A library of general utility functions
==================================================

Python Utility Library is a small collection of functions in several categories.

Date functions
==============

In order to use a date function you need to::

    import pyutillib.date_utils

Working with date strings
-------------------------

In order to have an unambiguous relation between a date in string and datetime
format, only a limited number of formats is available. The default is often 
good enough.

Usage examples::

    >>> import pyutillib.date_utils as du
    >>> du.datestr2date('20001231')
    datetime.date(2000, 12, 31)
    >>> du.datestr2date('12/31/2000')
    datetime.date(2000, 12, 31)
    >>> du.datestr2date('31-12-2000')
    datetime.date(2000, 12, 31)

    >>> import datetime
    >>> d = datetime.date(2000, 12, 31)
    >>> du.date2datestr(d)
    '20001231'
    >>> du.date2datestr(d, 'd-m-yy')
    '31-12-00'
    >>> du.date2datestr(d, 'd-m-yyy')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pyutillib/date_utils.py", line 128, in date2datestr
        raise ValueError('Invalid format string, year must have 2 or 4 digits')
    ValueError: Invalid format string, year must have 2 or 4 digits
    >>> du.date2datestr(d, 'mm/dd/yyyy')
    '12/31/2000'
    >>> du.date2datestr(d, 'yymmdd')
    '001231'

Working with weekdays
---------------------

These are simple things, but hard to remember, so just a few convenience 
functions::

    >>> import pyutillib.date_utils as du
    >>> import datetime as dt
    >>> du.is_weekday(dt.date(2013,4,16))
    True
    >>> du.is_weekday(dt.date(2013,4,14))
    False
    >>> du.is_weekend(dt.date(2013,4,14))
    True
    >>> du.is_weekend(dt.date(2013,4,16))
    False
    >>> du.next_weekday(dt.date(2013,4,16))
    datetime.date(2013, 4, 17)
    >>> du.next_weekday(dt.date(2013,4,12))
    datetime.date(2013, 4, 15)
    >>> du.next_weekday(dt.date(2013,4,13))
    datetime.date(2013, 4, 15)
    >>> du.previous_weekday(dt.date(2013,4,16))
    datetime.date(2013, 4, 15)
    >>> du.previous_weekday(dt.date(2013,4,15))
    datetime.date(2013, 4, 12)
    >>> du.previous_weekday(dt.date(2013,4,14))
    datetime.date(2013, 4, 12)

Working with years
------------------

Simple, but takes leap years into account::

    >>> import pyutillib.date_utils as du
    >>> import datetime as dt    >>> du.last_year(dt.date(2000,2,29))
    datetime.date(1999, 2, 28)
    >>> du.last_year(dt.date(2001,2,29))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: day is out of range for month
    >>> du.last_year(dt.date(2001,2,28))
    datetime.date(2000, 2, 28)
    >>> du.last_year(dt.date(2001,3,1))
    datetime.date(2000, 3, 1)


Math functions
==============

In order to use a math function you need to::

    import pyutillib.math_utils

Safe division
-------------

Sometimes you need to divide 2 numbers without worrying about division by zero.
the ``div`` function always returns a float, even if there is an iteger result.
Also the result of 0/0 is not mathematically correct, but often practically OK.

Some examples::

    >>> from pyutillib import math_utils as mu
    >>> mu.div(1,0)
    inf
    >>> mu.div(1,1)
    1.0
    >>> mu.div(0,0)
    0.0

Evaluating conditions
---------------------

This function can be used to evaluate conditions of arbitrary complexity. The
conditions need to be in a tuple format::

    (argument1, operator, argument2)

Where either argument 1 and 2 can be booleans if operator is a logical operator
('and', 'or'), or argument 1 and 2 are python objects if operator is a comparison
operator ('lt', 'le', 'eq', 'ne', 'ge', 'gt'). In the latter case both arguments
must be comparable, i.e. be of the same type. The only exception are floats and
ints, they can be compared with each other.

The outcome of each evaluation is always a boolean and they can be nested to
any level you like, by replacing a boolean argument by another tuple, e.g.::

    >>> from pyutillib import math_utils as mu
    >>> mu.eval_conditions(((6, 'gt', 5.7), 'and', True))
    True

It is possible to provide arguments by name, if you specify their value in a
dict::

    >>> arg_dict = {'a': 11, 'b': 0.24}
    >>> condition = ('a', 'eq', 'b')
    >>> mu.eval_conditions(condition, arg_dict)
    False

String functions
================

In order to use a string function you need to::

    import pyutillib.string_utils

Generating a random string
--------------------------

This function generates a random string of specified length made up of letters
and digits. A custom character set can be specified to limit (or extend) the
collection::

    >>> from pyutillib import string_utils as su
    >>> su.random_string()
    '7xgVQZxd'
    >>> su.random_string(charset='ABC+-')
    '-+-A+CBA'
    >>> su.random_string(20, 'ABC+-')
    'A+AB--BCB++CA-A++++C'

Safely evaluating strings
-------------------------

Instead of using eval, ast provides a better (safer) alternative. This function
is just a wrapper around that function to avoid exceptions::

    >>> su.safe_eval('(2,3,4)')
    (2, 3, 4)
    >>> print su.safe_eval('import os; os.name')
    None

Working with tuples and dicts in string format
----------------------------------------------

All functions below return None if the input string does not have the required
format.

Extracting a tuple from a string::

    >>> print su.str2tuple('(1,2,3)')
    (1, 2, 3)
    >>> print su.str2tuple('[1,2,3]')
    None
    >>> print su.str2tuple('hallo')
    None

Extracting a dict from a string::

    >>> print su.str2dict('{1:2, 3:4}')
    {1: 2, 3: 4}
    >>> print su.str2dict(' {1:2, 3:4}')
    None

Getting the keys from a dict in a string. The keys will be returned in
alphabetic order::

    >>> print su.str2dict_keys('{"a":1, 2:"3", -1: 0}')
    [-1, 2, 'a']
    >>> print su.str2dict_values('{"a":1, 2:"3", -1: 0}')
    [0, '3', 1]
