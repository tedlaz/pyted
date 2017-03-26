# -*- coding: utf-8 -*-

import unittest
import u_db as udb
import os


class Db_tests(unittest.TestCase):

    def setUp(self):
        self.db = 'ted1963.db'
        sql = "CREATE TABLE erg(id INTEGER PRIMARY KEY, epo TEXT NOT NULL, "
        sql += "ono TEXT, age INTEGER NOT NULL);\n"
        sql += "INSERT INTO erg VALUES(1, 'Laz', 'Ted', 52);\n"
        sql += "CREATE TABLE ta (id INTEGER PRIMARY KEY, per TEXT UNIQUE);\n"
        sql += "CREATE TABLE tb (id INTEGER PRIMARY KEY, "
        sql += "ta_id INTEGER, pdet TEXT UNIQUE);\n"
        udb.script(self.db, sql, True)

    def tearDown(self):
        os.remove(self.db)
        pass

    def test_is_list1_in_list2(self):
        ls1 = ['a1', 'a2']
        ls2 = ['a1', 'a2', 'a3']
        empty = []
        self.assertTrue(udb.is_list1_in_list2(ls1, ls2))
        self.assertFalse(udb.is_list1_in_list2(ls2, ls1))
        self.assertFalse(udb.is_list1_in_list2(empty, ls2))
        self.assertFalse(udb.is_list1_in_list2(ls1, empty))

    def test_fields_of_table(self):
        table = 'erg'
        flds = ['id', 'epo', 'ono', 'age']
        self.assertEqual(udb.fields_of_table(self.db, table), flds)
        self.assertEqual(udb.fields_of_table('aaa.db', table), [])
        self.assertEqual(udb.fields_of_table(self.db, 'tbll'), [])

    def test_save(self):
        dic = {'id': 0, 'epo': 'Laz', 'ono': 'Geo', 'age': 51}
        di2 = {'id': 1, 'epo': 'Daz', 'ono': 'Pop', 'age': 44}
        di3 = {'id': 2, 'epo': 'Daz', 'ono': 'Pop'}
        self.assertEqual(udb.save(self.db, 'erg', dic), 2)
        self.assertEqual(udb.save(self.db, 'erg', di2), 1)
        self.assertFalse(udb.save(self.db, 'ergw', dic))
        self.assertFalse(udb.save(self.db, 'erg', di3))
        sql = "SELECT count(epo) as count FROM erg"
        self.assertEqual(udb.select(self.db, sql), [{'count': 2}])

    def test_save_many(self):
        di1 = {'id': 0, 'epo': 'Laz', 'ono': 'Geo', 'age': 51}
        di2 = {'id': 1, 'epo': 'Daz', 'ono': 'Pop', 'age': 44}
        di3 = {'epo': 'Mav', 'ono': 'Nik', 'age': 52}
        di4 = {'epo': 'Daz', 'age': 44}
        self.assertTrue(udb.save_many(self.db, 'erg', [di1, di2, di3]))
        self.assertFalse(udb.save_many(self.db, 'erg', [di1, di2, di4]))

    def test_save_master_det(self):
        tmaster = 'ta'
        tdetail = 'tb'
        m1 = {'per': 'First master'}
        d1 = [{'pdet': 'master1 det1'}, {'pdet': 'master1 det2'}]
        db = self.db
        self.assertTrue(udb.save_master_det(db, tmaster, m1, tdetail, d1))
        m2 = {'per': 'Master Text'}
        d2 = [{'pdet': 'master2 det1'}, {'pdet': 'master2 det2'}]
        self.assertTrue(udb.save_master_det(db, tmaster, m2, tdetail, d2))
        d3 = [{'pdet': 'master3 det1'}, {'pdet': 'master3 det2'}]
        self.assertFalse(udb.save_master_det(db, tmaster, m1, tdetail, d3))
        self.assertFalse(udb.save_master_det(db, tmaster, m1, tdetail, ''))
        self.assertFalse(udb.save_master_det(db, tmaster, m1, '', d3))
        print(udb.select_table(db, 'ta'))
        print(udb.select_table(db, 'tb'))

    def test_select(self):
        adic = [{'id': 1, 'epo': 'Laz', 'ono': 'Ted', 'age': 52}]
        sql = 'select * from erg'
        self.assertEqual(udb.select(self.db, sql), adic)
        self.assertEqual(udb.select('ddsd.db', sql), [])
        self.assertEqual(udb.select(self.db, 'bullshit'), [])

    def test_select_table(self):
        adic = [{'id': 1, 'epo': 'Laz', 'ono': 'Ted', 'age': 52}]
        self.assertEqual(udb.select_table(self.db, 'erg'), adic)
        self.assertFalse(udb.select_table(self.db, 'ergq'))
        self.assertFalse(udb.select_table('adbegt', 'erg'))

    def test_sql_insert(self):
        dic = {'id': 0, 'epo': 'Mav', 'ono': 'Nic', 'age': 69}
        flds = ['id', 'epo', 'ono']
        rval = udb.sql_insert(dic, flds, 'erg')
        chval = "INSERT INTO erg (epo, ono) VALUES ('Mav', 'Nic');"
        self.assertEqual(rval, chval)
        self.assertEqual(udb.sql_insert(dic, flds, ''), '')
        self.assertEqual(udb.sql_insert('', flds, 'erg'), '')
        self.assertEqual(udb.sql_insert(dic, '', 'erg'), '')

    def test_script(self):
        sql = "BEGIN TRANSACTION;\n"
        sql += "INSERT INTO erg (epo, ono, age) VALUES ('Mav', 'Nic', 34);"
        sql += "INSERT INTO erg (epo, ono, age) VALUES ('Spa', 'Mix', 42);"
        self.assertTrue(udb.script(self.db, sql + 'COMMIT;'))
        sql += "INSERT INTO erg (epo, ono) VALUES ('Vas', 'Nik'); COMMIT;"
        self.assertFalse(udb.script(self.db, sql))
        sql2 = "SELECT count(epo) as count FROM erg;"
        self.assertEqual(udb.select(self.db, sql2), [{'count': 3}])


class Dict_tests(unittest.TestCase):

    def test_b(self):
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(Db_tests)
    # unittest.TextTestRunner(verbosity=2).run(suite)
