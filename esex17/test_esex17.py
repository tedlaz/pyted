import unittest
import ee


class Tests(unittest.TestCase):
    def test_01(self):
        self.assertEqual(ee.EKSODO, 2)
