import unittest
import tst


class Tests(unittest.TestCase):
    def test_01(self):
        self.assertEqual(tst.asa, 10)
