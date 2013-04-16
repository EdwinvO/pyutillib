'''
pyutillib/tests

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

import unittest
import datetime as dt

import pyutillib.date_utils as du
import pyutillib.math_utils as mu
import pyutillib.string_utils as su


class TestDateUtils(unittest.TestCase):
    '''
    '''

    def setUp(self):
        dd = dt.date
        self.validdata = (
            {'date': dd(2000,1,31), 'str': '20000131', 'fmt': 'yyyymmdd'},
            {'date': dd(2000,1,31), 'str': '000131', 'fmt': 'yymmdd'},
            {'date': dd(2000,1,31), 'str': '31-1-00', 'fmt': 'd-m-yy'},
            {'date': dd(2000,1,31), 'str': '31-1-2000', 'fmt': 'd-m-yyyy'},
            {'date': dd(2000,1,31), 'str': '31-01-00', 'fmt': 'dd-mm-yy'},
            {'date': dd(2000,1,31), 'str': '31-01-2000', 'fmt': 'dd-mm-yyyy'},
            {'date': dd(2000,1,31), 'str': '1/31/00', 'fmt': 'm/d/yy'},
            {'date': dd(2000,1,31), 'str': '1/31/2000', 'fmt': 'm/d/yyyy'},
            {'date': dd(2000,1,31), 'str': '01/31/00', 'fmt': 'mm/dd/yy'},
            {'date': dd(2000,1,31), 'str': '01/31/2000', 'fmt': 'mm/dd/yyyy'},
            )
        self.weekdays = (dd(2013,2,22), dd(2013,2,25), dd(2013,2,26), 
                dd(2013,2,27), dd(2013,2,28), dd(2013,3,1), dd(2013,3,4))
        self.weekend = (dd(2013,2,23), dd(2013,2,24), dd(2013,3,2), 
                dd(2013,3,3))

    def test_datestr2date(self):
        for data in self.validdata:
            self.assertEqual(du.datestr2date(data['str']), data['date'])

        invaliddateformats = ('1', '11', '111', '1111', '11111', '1111111',
            '111111111', '1111111111', '1111011', '1101111', 
            '031-1-00', '31-001-00', '31-1-000', '31-1-20001',
            'a1-1-00',
            )
        for date in invaliddateformats:
            self.assertRaises(ValueError, du.datestr2date, date)

        invaliddates = ('31/1/00', '01-31-00', '20010229')
        for date in invaliddates:
            self.assertRaises(ValueError, du.datestr2date, date)


    def test_date2datestr(self):
        #default fmt:
        self.assertEqual(du.date2datestr(self.validdata[0]['date']), 
                    self.validdata[0]['str'])
        #with format specifier
        for data in self.validdata:
            self.assertEqual(du.date2datestr(data['date'], data['fmt']), 
                    data['str'])
        invalidformats = ('dmy', 'd/m/y', 'dd/mm/yy', 'mm-dd-yy', 'yy-mm-dd',)
        date = dt.date(2000, 1, 31)
        for fmt in invalidformats:
            self.assertRaises(ValueError, du.date2datestr, date, fmt)


    def test_is_weekday(self):
        for date in self.weekdays:
            self.assertTrue(du.is_weekday(date))
        for date in self.weekend:
            self.assertFalse(du.is_weekday(date))


    def test_is_weekend(self):
        for date in self.weekdays:
            self.assertFalse(du.is_weekend(date))
        for date in self.weekend:
            self.assertTrue(du.is_weekend(date))


    def test_previous_weekday(self):
        for day1, day2 in ((8,7), (9,7), (10,7), (11,10), (12,11), (13,12), 
                           (14,13), (15,14), (16,14), (17,14)):
            self.assertEqual(du.previous_weekday(dt.date(2000,1,day1)), 
                    dt.date(2000,1,day2))


    def test_next_weekday(self):
        for day1, day2 in ((6, 7), (7, 10), (8,10), (9,10), (10,11), (11,12), 
                           (12,13), (13,14), (14,17), (15,17), (16,17)):
            self.assertEqual(du.next_weekday(dt.date(2000,1,day1)), 
                    dt.date(2000,1,day2))


    def test_last_year(self):
        self.assertEqual(du.last_year(dt.date(2000,3,29)), dt.date(1999,3,29))
        self.assertEqual(du.last_year(dt.date(2000,2,27)), dt.date(1999,2,27))
        self.assertEqual(du.last_year(dt.date(2000,2,29)), dt.date(1999,2,28))


class TestMathUtils(unittest.TestCase):

    def setUp(self):
        pass


    def test_div(self):
        self.assertEqual(mu.div(0,0), 0)
        self.assertEqual(mu.div(0,1), 0)
        self.assertEqual(mu.div(1,0), float('inf'))
        self.assertEqual(mu.div(2,1), 2.)
        self.assertEqual(mu.div(2,1.25), 1.6)
        self.assertEqual(mu.div(2,0.5), 4.)
        self.assertEqual(mu.div(0.5,0.25), 2.)
        self.assertEqual(mu.div(0.2, 0.1), 2.)


    def test_eval_conditions(self):
        self.assertTrue(mu.eval_conditions(None))
        self.assertRaises(TypeError, mu.eval_conditions, 'a')
        self.assertRaises(TypeError, mu.eval_conditions, (1,2,3,4))

        # simple conditions
        for conditions in ( (2, 'gt', 1), 
                            ('a', 'eq', 'a'),
                            ('a', 'lt', 'b'),
                            (2., 'gt', 1),
                            (1, 'eq', 1.),
                            (True, 'eq', True),
                            (True, 'or', False),
                            ):
            self.assertTrue(mu.eval_conditions(conditions), conditions)
        for conditions in ( (2, 'lt', 1), 
                            ('a', 'eq', 'b'),
                            (3, 'gt', 4.2),
                            (True, 'eq', False),
                            (True, 'and', False),
                            ):
            self.assertFalse(mu.eval_conditions(conditions), conditions)

        for conditions in ( 
                ('a', 'eq', 1),
                (True, 'eq', 3),
                (3, 'and', True),
                ):
            self.assertRaises(TypeError, mu.eval_conditions, conditions)

        for conditions in (
                (1, 'abc', 2),
                (1, 3, 2),
                ):
            self.assertRaises(ValueError, mu.eval_conditions, conditions)

        # simple conditions with data
        for conditions, data in ( (('x', 'lt', 2), {'x': 1}),
                                  (('y', 'eq', 1.3), {'y': 1.3}),
                                  (('y', 'and', True), {'y': True}),
                                 ):
            self.assertTrue(mu.eval_conditions(conditions, data), conditions)
        for conditions, data in ( (('x', 'lt', 1), {'x': 2}),
                                  (('x', 'eq', 1), {'x': 1.1}),
                                  ((True, 'and', 'abc'), {'abc': False}),
                                 ):
            self.assertFalse(mu.eval_conditions(conditions, data), conditions)
        for conditions, data in (
                (('x', 'gt', 1), {'y': 2}),
                ):
            self.assertRaises(TypeError, mu.eval_conditions, conditions, data)

        for conditions, data in (
                (('x', 'abc', 1), {'abc': 'and'}),
                ):
            self.assertRaises(ValueError, mu.eval_conditions, conditions, data)

        # complex conditions
        for conditions, data in (
                ((True, 'and', ('x', 'eq', 2)), {'x': 2}),
                (('x', 'eq', (1, 'ne', 'y')), {'x': True, 'y': 2}),
                                 ):
            self.assertTrue(mu.eval_conditions(conditions, data), conditions)
        for conditions, data in (
                ((('x', 'lt', 1), 'and', (2, 'lt', 'y')), {'x': 2, 'y': 1}),
                                 ):
            self.assertFalse(mu.eval_conditions(conditions, data), conditions)
        for conditions, data in (
                ((2, ('lt' , 'or', 'gt'), 1), {}),
                (('x', 'abc', 1), {'abc': 'and'}),
                                 ):
            self.assertRaises(ValueError, mu.eval_conditions, conditions, data)


class TestStringUtils(unittest.TestCase):

    def setUp(self):
        pass


    def test_random_string(self):
        # test default length
        self.assertEqual(len(su.random_string()), 8)
        # test length setting
        for length in xrange(5,10):
            self.assertEqual(len(su.random_string(length)), length)
        # test invalid lengths
        for length in (-2, -1, 0):
            self.assertRaises(ValueError, su.random_string, length)
        # test uniqueness - could theoretically fail, but very unlikely
        testlist = (su.random_string() for unused in xrange(10))
        self.assertEqual(len(set(testlist)), 10)
        # test default charset
        for c in su.random_string(10000):
            self.assertNotIn(c, '~!@#$%^&*()_+`-={}|[]\\:";\'<>?,./')
        # test charset - could theoretically fail, but very unlikely
        charset = 'ABC'
        abc = su.random_string(100, charset)
        self.assertEqual(set(abc), {'A', 'B', 'C'})


    def test_safe_eval(self):
        self.assertEqual(su.safe_eval('15'), 15)
        self.assertEqual(su.safe_eval('8.45'), 8.45)
        self.assertEqual(su.safe_eval('(1,2)'), (1,2))
        self.assertEqual(su.safe_eval('[1,2,3]'), [1,2,3])
        self.assertEqual(su.safe_eval("{'a':1, 4:'asdf'}"), {'a':1, 4:'asdf'})
        for s in ('raise SystemExit', 'import sys\n', '', '1y3', '[3,1', ''):
            self.assertIsNone(su.safe_eval(s))


    def test_str2dict(self):
        self.assertEqual(su.str2dict("{'a':1, 4:'asdf'}"), {'a':1, 4:'asdf'})
        self.assertIsNone(su.str2dict("{'a':1 4:'asdf'}"))
        self.assertIsNone(su.str2dict('raise SystemExit'))
        self.assertIsNone(su.str2dict('(1,2,3)'))


    def test_str2tuple(self):
        self.assertEqual(su.str2tuple("('a', 4, [1,2,3])"), ('a', 4, [1,2,3]))
        self.assertIsNone(su.str2tuple("['a', 4, {1.4,}]"))
        self.assertIsNone(su.str2tuple('raise SystemExit'))
        self.assertIsNone(su.str2tuple('(1)'))


    def test_get_dict_keys_values(self):
        dict_string = '{"a":1, 2:"3", -1: 0}'
        self.assertEqual(su.str2dict_values(dict_string), [0, '3', 1])
        self.assertIsNone(su.str2dict_values('asdf'))
        self.assertEqual(su.str2dict_keys(dict_string), [-1, 2, 'a'])
        self.assertIsNone(su.str2dict_keys('asdf'))


if __name__ == '__main__':
    unittest.main()
