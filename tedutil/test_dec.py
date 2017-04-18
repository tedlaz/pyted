"""
Testing module
"""
import unittest
import dec


class TestDec(unittest.TestCase):
    def test_01(self):
        self.assertEqual(float(dec.dec('12.34')), 12.34)

    def test_02(self):
        self.assertEqual(float(dec.dec(12.34)), 12.34)

    def test_03(self):
        self.assertEqual(float(dec.dec('12df')), 0)

    def test_04(self):
        self.assertEqual(float(dec.dec(None)), 0)

    def test_05(self):
        self.assertEqual(float(dec.dec(15.236344)), 15.24)


class TestDdi(unittest.TestCase):
    def test_01(self):
        vl1 = dec.Ddi(epo='Laz', _po1=10, _po2=12.346)
        vl2 = {'epo': 'Laz', '_po1': dec.dec(10), '_po2': dec.dec(12.35)}
        self.assertEqual(vl1, vl2)