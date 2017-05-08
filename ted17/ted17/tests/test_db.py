"""
Testing module
"""
import unittest
from ted17 import db


class TestDb(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_memorydb(self):
        sqm = 'CREATE TABLE ts(id INTEGER PRIMARY KEY, val TEXT);'
        sqd = 'CREATE TABLE dt(id INTEGER PRIMARY KEY, ts_id INTEGER, v TEXT);'
        sqli = ("INSERT INTO ts VALUES (1, 'ted');"
                "INSERT INTO ts VALUES (2, 'popi');"
                "INSERT INTO dt VALUES (1, 1, 'Val1');"
                "INSERT INTO dt VALUES (2, 1, 'val2');")
        sqls = "SELECT * FROM ts;"
        rv1 = [(1, 'ted'), (2, 'popi')]
        rv2 = (('id', 'val'), [(1, 'ted'), (2, 'popi')])
        rv3 = [{'id': 1, 'val': 'ted'}, {'id': 2, 'val': 'popi'}]
        rv4 = {'id': 1, 'val': 'ted',
               'zlines': [{'id': 1, 'v': 'Val1'}, {'id': 2, 'v': 'val2'}]}
        with db.SqliteManager(':memory:') as dbm:
            dbm.set_application_id(1235)
            self.assertEqual(dbm.application_id(), 1235)
            dbm.set_user_version(3242)
            self.assertEqual(dbm.user_version(), 3242)
            dbm.script(sqm + sqd)
            dbm.script(sqli)
            self.assertEqual(dbm.select(sqls), rv1)
            self.assertEqual(dbm.select_with_names(sqls), rv2)
            self.assertEqual(dbm.select_as_dict(sqls), rv3)
            self.assertEqual(dbm.select_master_detail_as_dic(1, 'ts', 'dt'), rv4)

    def test_tables(self):
        sqm = ("CREATE TABLE ts(id INTEGER PRIMARY KEY, val TEXT);"
               "CREATE TABLE dt(id INTEGER PRIMARY KEY, ts_id INTEGER, v TEXT);"
               "INSERT INTO ts VALUES (1, 'ted');"
               "INSERT INTO ts VALUES (2, 'popi');"
               "INSERT INTO dt VALUES (1, 1, 'Val1');"
               "INSERT INTO dt VALUES (2, 1, 'val2');")
        with db.SqliteManager(':memory:') as dbm:
            dbm.script(sqm)
            self.assertEqual(dbm.tables(), ('dt', 'ts'))
            self.assertEqual(dbm.fields('dt'), ('id', 'ts_id', 'v'))
