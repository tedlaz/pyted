# -*- coding: utf-8 -*-
import os
import unittest
from date2str import date2str
from dec import dec
from dec2str import dec2str
from distd import distd
from distl import distl
from eucdist import eucdist
from grup import grup
from isvat import isvat
from iszerol import iszerol
from listadd import listadd
from listdif import listdif
from listdim import listdim


class Function_tests(unittest.TestCase):

    def tearDown(self):
        # os.remove('./date2str.pyc')
        pass

    def test_date2str(self):
        self.assertEqual(date2str('2016-12-31'), '31/12/2016')
        self.assertEqual(date2str('2016-08-05'), '5/8/2016')
        self.assertEqual(date2str('2016-08-05', False), '05/08/2016')

    def test_dec(self):
        self.assertEqual(dec('ted'), 0)
        self.assertEqual(float(dec(1.23)), 1.23)
        self.assertEqual(float(dec('1.234')), 1.23)
        self.assertEqual(float(dec('1.235')), 1.24)

    def test_dec2str(self):
        self.assertEqual(dec2str('123456.45'), '123.456,45')
        self.assertEqual(dec2str('-123456.45'), '-123.456,45')
        self.assertEqual(dec2str('-0'), '0,00')

    def test_distd(self):
        f = {'k': 20, 'b': 10, 'c': 30, 'd': 40}
        fv = {'k': dec(20), 'b': dec(10), 'c': dec(30), 'd': dec(40)}
        self.assertEqual(distd(100, f), fv)

    def test_distl(self):
        d = [10, 20, 30, 40]
        f = [dec(10), dec(20), dec(30), dec(40)]
        self.assertEqual(distl(100, d), f)

    def test_eucdist(self):
        self.assertEqual(eucdist(0, [3, 4, 0]), 5.0)
        self.assertEqual(eucdist([0, 0, 0, 0, 0], [0, 0, 3, 4, 0]), 5.0)

    def test_grup(self):
        self.assertEqual(grup(u'Δοκιμή'), u'ΔΟΚΙΜΗ')
        self.assertEqual(grup(u'kalimera'), u'KALIMERA')

    def test_isvat(self):
        self.assertEqual(isvat('513111172'), True)
        self.assertEqual(isvat('513111173'), False)

    def test_iszerol(self):
        self.assertEqual(iszerol([0, 0, 0, 0]), True)
        self.assertEqual(iszerol([0, 0, 0, 5]), False)

    def test_listadd(self):
        self.assertEqual(listadd([1, 2], [10, 20]), [dec(11), dec(22)])
        self.assertEqual(listadd([1, 'a', 3], [10, 20]), [dec(11), dec(20), dec(3)])
        self.assertEqual(listadd([1, 2], 4), [dec(5), dec(2)])

    def test_listdif(self):
        self.assertEqual(listdif([1, 2], [10, 20]), [dec(-9), dec(-18)])
        self.assertEqual(listdif([10, 20], [1, 2]), [dec(9), dec(18)])
        self.assertEqual(listdif([10, 20], 1), [dec(9), dec(20)])

    def test_listdim(self):
        self.assertEqual(listdim([1, 2], [10]), ([1, 2], [10, 0]))
        self.assertEqual(listdim([1, 2], 10), ([1, 2], [10, 0]))


if __name__ == '__main__':
    unittest.main()
