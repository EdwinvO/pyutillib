'''
pyutillib/date_utils.py

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

import datetime


VALID_DATE_FORMATS_TEXT = '''The following date formats are valid:
    yymmdd    yyyymmdd
    d-m-yy    d-m-yyyy
    m/d/yy    m/d/yyyy
Where in the latter 4 formats m and d may be 1 or 2 digits which may include
a leading zero.
In case of a 2-digit year, it is assumed to be after 2000'''


def datestr2date(date_str):
    '''
    Turns a string into a datetime.date object. This will only work if the 
    format can be "guessed", so the string must have one of the formats from
    VALID_DATE_FORMATS_TEXT.

    Args:
        date_str (str) a string that represents a date
    Returns:
        datetime.date object
    Raises:
        ValueError if the input string does not have a valid format.
    '''
    if any(c not in '0123456789-/' for c in date_str):
        raise ValueError('Illegal character in date string')
    if '/' in date_str:
        try:
            m, d, y = date_str.split('/')
        except:
            raise ValueError('Date {} must have no or exactly 2 slashes. {}'.
                    format(date_str, VALID_DATE_FORMATS_TEXT))
    elif '-' in date_str:
        try:
            d, m, y = date_str.split('-')
        except:
            raise ValueError('Date {} must have no or exactly 2 dashes. {}'.
                    format(date_str, VALID_DATE_FORMATS_TEXT))
    elif len(date_str) == 8 or len(date_str) == 6:
        d = date_str[-2:]
        m = date_str[-4:-2]
        y = date_str[:-4]
    else:
        raise ValueError('Date format not recognised. {}'.format(
                VALID_DATE_FORMATS_TEXT))
    if len(y) == 2:
        year = 2000 + int(y)
    elif len(y) == 4:
        year = int(y)
    else:
        raise ValueError('year must be 2 or 4 digits')
    for s in (m, d):
        if 1 <= len(s) <= 2:
            month, day = int(m), int(d)
        else:
            raise ValueError('m and d must be 1 or 2 digits')
    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise ValueError('Invalid date {}. {}'.format(date_str, 
                VALID_DATE_FORMATS_TEXT))


def date2datestr(date, fmt='yyyymmdd'):
    '''
    Turns a datetime.date object into a string. The string must have one of the
    formats from VALID_DATE_FORMATS_TEXT to make it compatible with 
    datestr2date.

    Args:
        date (datetime.date) the date to be translated
        fmt (str) a format string.
    Returns:
        (str) that represents a date.
    Raises:
        ValueError if the format is not valid.
    '''
    if '-' in fmt:
        if not fmt.index('d') < fmt.index('m') < fmt.index('y'):
            raise ValueError('Invalid format string. {}'.format(
                    VALID_DATE_FORMATS_TEXT))
        d, m, y = fmt.split('-')
    elif '/' in fmt:
        if not fmt.index('m') < fmt.index('d') < fmt.index('y'):
            raise ValueError('Invalid format string. {}'.format(
                    VALID_DATE_FORMATS_TEXT))
        m, d, y = fmt.split('/')
    elif any(c not in 'dmy' for c in fmt):
        raise ValueError('Invalid character in format string. {}'.format(
                VALID_DATE_FORMATS_TEXT))
    else:
        if not fmt.index('y') < fmt.index('m') < fmt.index('d'):
            raise ValueError('Invalid format string. {}'.format(
                    VALID_DATE_FORMATS_TEXT))
        y, m, d = fmt[:-4], fmt[-4:-2], fmt[-2:]
    for string, char in ((d, 'd'), (m, 'm'), (y, 'y')):
        if any(c != char for c in string):
            raise ValueError('Invalid date format: {} is not {}'.\
                    format(char, string))
    if len(y) == 4:
        fmt = fmt.replace('yyyy', '%Y', 1)
    elif len(y) == 2:
        fmt = fmt.replace('yy', '%y', 1)
    else:
        raise ValueError('Invalid format string, year must have 2 or 4 digits')
    if len(m) == 2:
        fmt = fmt.replace('mm', '%m', 1)
    elif len(m) == 1:
        fmt = fmt.replace('m', 'X%m', 1)
    else:
        raise ValueError('Invalid format string, month must have 1 or 2 digits')
    if len(d) == 2:
        fmt = fmt.replace('dd', '%d', 1)
    elif len(d) == 1:
        fmt = fmt.replace('d', 'X%d', 1)
    else:
        raise ValueError('Invalid format string, day must have 1 or 2 digits')
    return date.strftime(fmt).replace('X0','X').replace('X','')


def is_weekday(date):
    '''
    Returns a boolean that indicates if date is a weekday.

    Args:
        date (datetime or datetime.date)
    Returns:
        (boolean)
    Raises:
        -
    '''
    return True if date.weekday() < 5 else False


def is_weekend(date):
    '''
    Returns a boolean that indicates if date is in a weekend.

    Args:
        date (datetime or datetime.date)
    Returns:
        (boolean)
    Raises:
        -
    '''
    return not is_weekday(date)


def previous_weekday(date):
    '''
    Returns the last weekday before date

    Args:
        date (datetime or datetime.date)
    Returns:
        (datetime or datetime.date)
    Raises:
        -
    '''
    weekday = date.weekday()
    if weekday == 0:
        n_days = 3
    elif weekday == 6:
        n_days = 2
    else:
        n_days = 1
    return date - datetime.timedelta(days=n_days)


def next_weekday(date):
    '''
    Return the first weekday after date

    Args:
        date (datetime or datetime.date)
    Returns:
        (datetime or datetime.date)
    Raises:
        -
    '''
    n_days = 7 - date.weekday()
    if n_days > 3:
        n_days = 1
    return date + datetime.timedelta(days=n_days)


def last_year(date_):
    '''
    Returns the same date 1 year ago.

    Args:
        date (datetime or datetime.date)
    Returns:
        (datetime or datetime.date)
    Raises:
        -
    '''
    day = 28 if date_.day == 29 and date_.month == 2 else date_.day
    return datetime.date(date_.year-1, date_.month, day)
