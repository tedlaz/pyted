"""TESTING utils.py"""
import unittest
from decimal import Decimal
import utils as ul


class TestUtils(unittest.TestCase):

    def test_grup(self):
        self.assertEqual(ul.grup('εδώted123'), 'ΕΔΩTED123')

    def test_isNum(self):
        self.assertEqual(ul.isNum(10.23), True)
        self.assertEqual(ul.isNum('ted'), False)

    def test_dec(self):
        # self.assertEqual(ul.dec(12.245), ul.dec(12.25))
        self.assertEqual(ul.dec(12.345), ul.dec(12.35))
        self.assertEqual(ul.dec('popi'), Decimal(0))
        self.assertEqual(ul.dec(None), Decimal(0))

    def test_dec2text_flat(self):
        self.assertEqual(ul.dec2text_flat(12.34, '1234')
        self.assertEqual(ul.dec2text_flat(12, '1200')

    def test_iso_number_from_greek(self):
        self.assertEqual(ul.iso_number_from_greek('123.456,78'), '123456.78')

    def test_dec2gr(self):
        self.assertEqual(ul.dec2gr(14.28), '14,28')
        self.assertEqual(ul.dec2gr(14.2), '14,20')
        self.assertEqual(ul.dec2gr(123456.78), '123.456,78')
        self.assertEqual(ul.dec2gr(-123456.78), '-123.456,78')

    def test_iso_date_from_greek(self):
        self.assertEqual(ul.iso_date_from_greek('10/02/1963'), '1963-02-10')
        self.assertEqual(ul.iso_date_from_greek('9/2/1963'), '1963-02-09')

    def test_remove_simple_quotes(self):
        self.assertEqual(ul.remove_simple_quotes("thi's al's"), 'this als')

    def test_getymd_from_iso(self):
        self.assertEqual(ul.getymd_from_iso('2015-01-12'), (2015, 1, 12))

    def test_print_dicl(self):
        di1 = {'epo': 'Λάζαρος', 'val': 100}
        dil = {'epo': 'Επώνυμο', 'val': 'Τιμή'}
        # ul.print_dicl([di1, dil], '20', '<12')
        # ul.print_dicl([di1, dil], '20', '>12')
        # ul.print_dicl([di1, dil], '20', '^12')

    def test_dicdec(self):
        aa = ul.DicDec()
        aa['fpa'] = 100
        aa['poso'] = 'ted'
        self.assertEqual(aa, {'fpa': Decimal(100), 'poso': Decimal(0)})

    def test_required_keys(self):
        ke1 = ['k1', 'k2']
        vl1 = {'k1': 1, 'k2': 2, 'k3': 3}
        self.assertEqual(ul.has_keys(ke1, vl1), True)
        vl2 = {'k1': 1, 'k3': 3}
        self.assertRaises(ul.RequiredKeyException, ul.has_keys, ke1, vl2)
