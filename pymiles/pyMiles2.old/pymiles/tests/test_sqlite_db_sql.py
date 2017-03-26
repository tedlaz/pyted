# -*- coding: utf-8 -*-
import unittest
from pymiles.sqlite import db_sql as ds


class Dbtests(unittest.TestCase):

    def setUp(self):
        # Initialize data
        pass

    def tearDown(self):
        # Clean up finally
        pass

    def test_save_insert(self):
        table = 'erg'
        flds = {'id': 0, 'epo': 'ted', 'ono': 'popi'}
        fval = "INSERT INTO erg (epo, ono) VALUES ('ted', 'popi');"
        self.assertEqual(ds.save(table, flds), fval)

    def test_save_update(self):
        table = 'erg'
        flds = {'id': 1, 'epo': 'ted', 'ono': 'popi'}
        fval = "UPDATE erg set epo='ted', ono='popi' WHERE id=1;"
        self.assertEqual(ds.save(table, flds), fval)

if __name__ == '__main__':
    unittest.main()
