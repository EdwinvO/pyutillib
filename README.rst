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

Usage ::

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

there is more...
----------------
TODO

Math functions
==============

TODO

String functions
==============

TODO