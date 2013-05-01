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
    >>> import datetime as dt
    >>> du.last_year(dt.date(2000,2,29))
    datetime.date(1999, 2, 28)
    >>> du.last_year(dt.date(2001,2,29))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: day is out of range for month
    >>> du.last_year(dt.date(2001,2,28))
    datetime.date(2000, 2, 28)
    >>> du.last_year(dt.date(2001,3,1))
    datetime.date(2000, 3, 1)

The DateList class
------------------

This class subclasses the standard Python list, so all normal list functionality
is available. The differences are that there are a few extra methods and that
the .index method works differently.

**Instantiating:** a list of dates works as expected::

    >>> import pyutillib.date_utils as du
    >>> import datetime as dt
    >>> dates = [dt.date(2012, 1, d) for d in range(1, 32)]
    >>> dl = du.DateList(dates)
    >>> dl[0]
    datetime.date(2012, 1, 1)
    >>> dl[-1]
    datetime.date(2012, 1, 31)

**index** returns the the index of a date, or (if the date is not in the list), 
the index of the most recent date before the input date::

    >>> dl.index(dt.date(2012,1,2))
    1
    >>> dl.index(dt.date(2012,1,30))
    29
    >>> dates2 = [dt.date(2012, 1, d) for d in range(1, 32, 4)]
    >>> dl2 = du.DateList(dates2)
    >>> for d in dl2: print d
    2012-01-01
    2012-01-05
    2012-01-09
    2012-01-13
    2012-01-17
    2012-01-21
    2012-01-25
    2012-01-29
    >>> dl2.index(dt.date(2012,1,8))
    1
    >>> dl2.index(dt.date(2012,1,9))
    2
    >>> dl2.index(dt.date(2012,1,10))
    2

**on_or_before** returns the input date, or (if the date is not in the list), 
the most recent date before the input date::

    >>> dl2.on_or_before(dt.date(2012,1,5))
    datetime.date(2012, 1, 5)
    >>> dl2.on_or_before(dt.date(2012,1,4))
    datetime.date(2012, 1, 1)
    >>> dl2.on_or_before(dt.date(2012,1,6))
    datetime.date(2012, 1, 5)

**delta** returns the number of days in the list between two dates::

    >>> dl.delta(dt.date(2012,1,10), dt.date(2012,1,20))
    10
    >>> dl2.delta(dt.date(2012,1,10), dt.date(2012,1,20))
    2

**offset** returns the date n_days after (or before if n_days < 0) the input
date, note that these are not calendar days, but dates in the list::

    >>> dl.offset(dt.date(2012,1,10),3)
    datetime.date(2012, 1, 13)
    >>> dl2.offset(dt.date(2012,1,10),3)
    datetime.date(2012, 1, 21)

**subset** returns a list of dates between two specified dates, only dates that
are in the original list are included::

    >>> for d in dl.subset(dt.date(2012,1,10), dt.date(2012,1,20)): print d
    2012-01-10
    2012-01-11
    2012-01-12
    2012-01-13
    2012-01-14
    2012-01-15
    2012-01-16
    2012-01-17
    2012-01-18
    2012-01-19
    2012-01-20
    >>> for d in dl2.subset(dt.date(2012,1,10), dt.date(2012,1,20)): print d
    2012-01-13
    2012-01-17

Working with time strings
-------------------------

In order to have an unambiguous relation between a time in string and 
datetime.time format, only a limited number of formats is available. The 
default is often good enough.

Usage examples::

    >>> from pyutillib import date_utils as du
    >>> du.timestr2time('123456')
    datetime.time(12, 34, 56)
    >>> du.timestr2time('12:34:56')
    datetime.time(12, 34, 56)
    >>> du.timestr2time('12:34')
    datetime.time(12, 34)
    >>> du.timestr2time('01:23')
    datetime.time(1, 23)
    >>> du.timestr2time('1:23')
    datetime.time(1, 23)
    
    >>> import datetime
    >>> t = datetime.time(23,59,59)
    >>> du.time2timestr(t)
    hhmmss 23:59:59
    '235959'
    >>> du.time2timestr(t, 'hh:mm')
    hh:mm 23:59:59
    '23:59'
    >>> du.time2timestr(t, 'hh:mm:ss')
    hh:mm:ss 23:59:59
    '23:59:59'
    >>> t = datetime.time(5,59,59)
    >>> du.time2timestr(t)
    hhmmss 05:59:59
    '055959'
    >>> du.time2timestr(t, 'hh:mm:ss')
    hh:mm:ss 05:59:59
    '05:59:59'
    >>> du.time2timestr(t, 'h:mm:ss')
    h:mm:ss 05:59:59
    '5:59:59'
    >>> du.time2timestr(t, 'h:mm')
    h:mm 05:59:59
    '5:59'
    >>> du.time2timestr(t, 'hmmss')
    hmmss 05:59:59
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pyutillib/date_utils.py", line 383, in time2timestr
        else:
    ValueError: Invalid character in format string. The following time formats are valid:
        hhmmss
        hh:mm:ss    h:mm:ss
        hh:mm       h:mm
    Where in the latter 2 formats hh has d digits which may include a leading zero
    and h may have 1 or 2 digits and no leading zero. 
    h/hh is always in 24 hour clock.

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

Translating a decimal string to an int
--------------------------------------

This function takes a string that represents a decimal number and returns an 
integer. The *decimals* argument allows you to 'shift the decimal point', e.g.::

    >>> from pyutillib import string_utils as su
    >>> su.decstr2int('123.456', 3)
    123456
    >>> su.decstr2int('123.456', 2)
    12345
    >>> su.decstr2int('123.456', 4)
    1234560
    >>> su.decstr2int('123', 4)
    1230000
    >>> su.decstr2int('123.456', -1)
    12

Note from the above examples that the input string does not need to contain a 
decimal point and also the decimals argument may be negative (or 0).
