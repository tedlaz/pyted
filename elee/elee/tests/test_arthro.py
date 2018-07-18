import unittest
from elee import arthro as ar


class Tests(unittest.TestCase):
    def setUp(self):
        self.ar1 = ar.Arthro('2018-01-01', 'ΤΔΑ12', 'Αγορές εμπορευμάτων')
        self.ar1.add_line('20.01.2024', 100, 0)
        self.ar1.add_line('54.00.2024', 24, 0)

    def tearDown(self):
        del self.ar1

    def test_01(self):
        self.assertFalse(self.ar1.is_complete)

    def test_02(self):
        self.ar1.add_line('50.00.0001', 0, 124)
        self.assertTrue(self.ar1.is_complete)

    def test_03(self):
        self.ar1.add_line('50.00.0001', 0, 124)
        self.assertEqual(self.ar1.ypoloipo, 0)
