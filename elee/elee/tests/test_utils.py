import unittest
from elee import utils as ul


class Tests(unittest.TestCase):
    def test_isAfm_01(self):
        self.assertTrue(ul.is_afm('046949583'))

    def test_isAfm_02(self):
        self.assertFalse(ul.is_afm('04694958f'))

    def test_isAfm_03(self):
        # Less than 9 digits
        self.assertFalse(ul.is_afm('04694'))

    def test_isAfm_04(self):
        # More than 9 digits
        self.assertFalse(ul.is_afm('0469495834'))

    def test_starts_with_05(self):
        self.assertTrue(ul.starts_with('Test', 't|T'))

    def test_starts_with_06(self):
        self.assertFalse(ul.starts_with('Test', 't|e|d'))

    def test_starts_with_07(self):
        self.assertTrue(ul.starts_with('54.00.00', '54.00|3'))

    def test_starts_with_08(self):
        self.assertFalse(ul.starts_with(5400, '54|3'))  # only strings allowed

    def test_starts_with_09(self):
        self.assertTrue(ul.starts_with('Test', 'T'))

    def test_match_01(self):
        self.assertTrue(ul.match('20.00.00.024', '2?.??.??.?24'))

    def test_match_02(self):
        self.assertFalse(ul.match('20.00.00.018', '2?.??.??.?24'))

    def test_match_03(self):
        # test size
        self.assertFalse(ul.match('20.00.00.24', '2?.??.??.?24'))

    def test_match_04(self):
        self.assertTrue(ul.match('20.00.00.024', '*.024'))

    def test_match_05(self):
        self.assertTrue(ul.match('20.00.00.24', '20.00.*'))

    def test_match_06(self):
        self.assertFalse(ul.match('20.00.00.23', '*.024'))
