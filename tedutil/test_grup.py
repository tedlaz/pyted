"""
Testing module
"""
import unittest
import grup


class TestGrup(unittest.TestCase):
    def test_01(self):
        self.assertEqual(grup.grup('θεόδωρος'), 'ΘΕΟΔΩΡΟΣ')

    def test_02(self):
        self.assertEqual(grup.grup('εύλογίας'), 'ΕΥΛΟΓΙΑΣ')

    def test_03(self):
        self.assertEqual(grup.grup('δυϊσμός'), 'ΔΥΪΣΜΟΣ')

    def test_04(self):
        self.assertEqual(grup.grup('ΰΐϋ'), 'ΫΪΫ')

    def test_05(self):
        self.assertEqual(grup.grup('tedλαζα'), 'TEDΛΑΖΑ')