"""TESTING foroi.py"""
import unittest
from decimal import Decimal
import foroi as fr

tst1 = {'forologiteo': Decimal('32458.00'),
        'paidia': 3,
        'typos': 'Μισθωτοί',
        'forosKlimakas': Decimal('8209.46'),
        'meiosi': 1975.42,
        'forosa': Decimal('6234.04'),
        'forosp': Decimal('6140.53'),
        'ekptosi': Decimal('93.51'),
        'eea': Decimal('835.77'),
        'katharo': Decimal('25481.70'),
        'xrisi': 2017}


class TestForoi(unittest.TestCase):
    def test_foros(self):
        self.assertEqual(fr.foros_eisodimatos(2017, 32458, 3), tst1)
        # print('Testing function foroi.printfor')
        # fr.printfor(2017, 49000, 50000, 500)
