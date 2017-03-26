# -*- coding: utf-8 -*-


import unittest
import u_sql as usql
from collections import OrderedDict as odi


class Sql_tests(unittest.TestCase):

    def setUp(self):
        self.dic1 = odi([('epo', 'Laz'), ('ono', 'Ted'), ('age', 53)])
        self.tbl = 'erg'
        self.r = "INSERT INTO erg (epo, ono, age) VALUES ('Laz', 'Ted', '53');"
        self.dic2 = odi([('id', 3), ('epo', 'Laz'), ('ono', 'Ted')])
        self.rv2 = "UPDATE erg set epo='Laz', ono='Ted' WHERE id=3;"

    def test_insert(self):
        self.assertEqual(usql._insert(self.tbl, self.dic1), self.r)

    def test_update(self):
        self.assertEqual(usql._update(self.tbl, self.dic2), self.rv2)

    def test_save(self):
        self.assertEqual(usql.save(self.tbl, self.dic1), self.r)
        self.assertEqual(usql.save(self.tbl, self.dic2), self.rv2)

    def test_save_list(self):
        lst = [self.dic1, self.dic2]
        rv = [self.r, self.rv2]
        self.assertEqual(usql.save_list(self.tbl, lst), rv)

    def test_save_many(self):
        lst = [self.dic1, self.dic2]
        rv = self.r + '\n' + self.rv2 + '\n'
        self.assertEqual(usql.save_many(self.tbl, lst), rv)

    def test_save_many_tran(self):
        lst = [self.dic1, self.dic2]
        rv = "BEGIN TRANSACTION;\n"
        rv += self.r + '\n' + self.rv2 + '\n'
        rv += "COMMIT;"
        self.assertEqual(usql.save_many_tran(self.tbl, lst), rv)


if __name__ == '__main__':
    unittest.main()
