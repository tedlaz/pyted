"""TESTING payroll_tameia.py"""
import unittest
import payroll_tameia as pt
import utils as ul


class TestPayrollTameia(unittest.TestCase):
    def test_ika(self):
        nik = {'poso': 100, 'pika': .45, 'pikae': .15}
        self.assertEqual(pt.ika(nik)[0]['ika'], ul.dec(45))
        nik = {'poso': 100, 'pika': 45, 'pikae': 15}
        self.assertEqual(pt.ika(nik)[0]['ika'], ul.dec(45))
