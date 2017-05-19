"""
Testing module
"""
import unittest
from ted17 import dec


class TestDec(unittest.TestCase):

    def test_isNum_01(self):
        self.assertEqual(dec.isNum('12.35'), True)

    def test_isNum_02(self):
        self.assertEqual(dec.isNum('12,35'), False)

    def test_isNum_03(self):
        self.assertEqual(dec.isNum('12.35a'), False)

    def test_isNum_04(self):
        self.assertEqual(dec.isNum('-0'), True)

    def test_dec_01(self):
        self.assertEqual(float(dec.dec('12.34')), 12.34)

    def test_dec_02(self):
        self.assertEqual(float(dec.dec(12.34)), 12.34)

    def test_dec_03(self):
        self.assertEqual(float(dec.dec('12df')), 0)

    def test_dec_04(self):
        self.assertEqual(float(dec.dec(None)), 0)

    def test_dec_05(self):
        self.assertEqual(float(dec.dec(15.236344)), 15.24)

    def test_dec_06(self):
        self.assertNotEqual(float(dec.dec('tedd')), 1)

    def test_triades_01(self):
        self.assertEqual(dec.triades('abcdef'), 'abc.def')

    def test_triades_02(self):
        self.assertEqual(dec.triades('abcdefg'), 'a.bcd.efg')

    def test_triades_03(self):
        self.assertEqual(dec.triades('abcdefg', '|'), 'a|bcd|efg')

    def test_triades_04(self):
        self.assertEqual(dec.triades('ab'), 'ab')

    def test_triades_05(self):
        self.assertEqual(dec.triades(''), '')

    def test_dec2gr_01(self):
        self.assertEqual(dec.dec2gr('-2456', 1), '-2.456,0')

    def test_dec2gr_02(self):
        self.assertEqual(dec.dec2gr('-0', 0), '0')

    def test_dec2gr_03(self):
        self.assertEqual(dec.dec2gr('123123123.45'), '123.123.123,45')

    def test_gr2dec_01(self):
        self.assertEqual(dec.gr2dec('123.123.123,45'), dec.dec('123123123.45'))

    def test_Ddi_01(self):
        vl1 = dec.Ddi(epo='Laz', _po1=10, _po2=12.346)
        vl2 = {'epo': 'Laz', '_po1': dec.dec(10), '_po2': dec.dec(12.35)}
        self.assertEqual(vl1, vl2)

    def test_distribute_01(self):
        dlist = [10, 20, 30, 40]
        rlist = (dec.dec(10), dec.dec(20), dec.dec(30), dec.dec(40))
        self.assertEqual(dec.distribute(100, dlist), rlist)

    def test_distribute_02(self):
        self.assertEqual(dec.distribute(10.34, [12.35, ]), (dec.dec(10.34), ))

    def test_print(self):
        print(dec.dec('200'))
