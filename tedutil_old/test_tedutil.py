# -*- coding: utf-8 -*-
from tedutil_old import ted_util as tu
import unittest


class Tedutil_tests(unittest.TestCase):

    def test_dec1(self):
        self.assertEqual(tu.dec('2.23444'), tu.dec(2.23))

    def test_dec2(self):
        self.assertEqual(tu.dec('2.23444a'), tu.dec('0.0'))

    def test_dec3(self):
        self.assertEqual(tu.dec('-2.23444'), tu.dec(-2.23))

    def test_dec2gr(self):
        self.assertEqual(tu.dec2gr('123456789.012'), '123.456.789,01')

    def test_dec2gr2(self):
        self.assertEqual(tu.dec2gr('-123456789.012'), '-123.456.789,01')

    def test_dec2gr3(self):
        self.assertEqual(tu.dec2gr('0', 0, True), '')

    def test_dec2gr4(self):
        self.assertEqual(tu.dec2gr('0', 0, False), '0')

    def test_dec2gr5(self):
        self.assertEqual(tu.dec2gr('0', 3, False), '0,000')

    def test_date2gr1(self):
        self.assertEqual(tu.date2gr('2015-01-25'), '25/1/2015')

    def test_date2gr2(self):
        self.assertEqual(tu.date2gr('2015-10-05'), '5/10/2015')

    def test_date2gr3(self):
        self.assertFalse(tu.date2gr('2015-12-31') == '32/12/2015')

    def test_date2str1(self):
        self.assertEqual(tu.date2str('2012-11-28', 'dfd'), '20121128')

    def test_date2str2(self):
        self.assertEqual(tu.date2str('2012-11-28', 'dmy'), '28112012')

    def test_date2str3(self):
        self.assertEqual(tu.date2str('2012-11-28', 'dym'), '28201211')

    def test_date2str4(self):
        self.assertEqual(tu.date2str('2012-11-28', 'mdy'), '11282012')

    def test_date2str5(self):
        self.assertEqual(tu.date2str('2012-11-28', 'myd'), '11201228')

    def test_date2str6(self):
        self.assertEqual(tu.date2str('2012-11-28', 'ymd'), '20121128')

    def test_date2str7(self):
        self.assertEqual(tu.date2str('2012-11-28', 'ydm'), '20122811')

    def test_null2zero1(self):
        self.assertEqual(tu.nul2zero(''), 0)

    def test_null2zero2(self):
        self.assertEqual(tu.nul2zero(None), 0)

    def test_grupper1(self):
        self.assertEqual(tu.grupper('ted'), 'TED')

    def test_grupper2(self):
        self.assertEqual(tu.grupper(u'Θόδωρος'), u'ΘΟΔΩΡΟΣ')

    def test_grupper3(self):
        self.assertEqual(tu.grupper(u'Άλέξίτής'), u'ΑΛΕΞΙΤΗΣ')
if __name__ == '__main__':
    unittest.main()
