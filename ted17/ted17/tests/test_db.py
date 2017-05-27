"""
Testing module
"""
import unittest
import os
from ted17 import db

DBTEST = 'test_database.db'

SQL_CREATE = """CREATE TABLE ts(id INTEGER PRIMARY KEY, val TEXT);
CREATE TABLE dt(id INTEGER PRIMARY KEY, ts_id INTEGER, v TEXT);
CREATE TABLE zlbl(fld TEXT PRIMARY KEY, lbl TEXT NOT NULL UNIQUE);
INSERT INTO zlbl VALUES ('id', 'ΑΑ');
INSERT INTO ts VALUES (1, 'ted');
INSERT INTO ts VALUES (2, 'popi');
INSERT INTO dt VALUES (1, 1, 'Val1');
INSERT INTO dt VALUES (2, 1, 'val2');"""


def setUpModule():
    db.create_db(DBTEST, SQL_CREATE, 1963, 2017001)


def tearDownModule():
    os.remove(DBTEST)


class TestDb(unittest.TestCase):
    """Varius tests"""
    def test_memorydb(self):
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
            dbm.script(SQL_CREATE)
            self.assertEqual(dbm.select(sqls), rv1)
            self.assertEqual(dbm.select(sqls, 'names-tuples'), rv2)
            self.assertEqual(dbm.select(sqls, 'dicts'), rv3)
            self.assertEqual(dbm.select_md(1, 'ts', 'dt'), rv4)

    def test_tables(self):
        with db.SqliteManager(':memory:') as dbm:
            dbm.script(SQL_CREATE)
            self.assertEqual(dbm.tables(), ('dt', 'ts', 'zlbl'))
            self.assertEqual(dbm.fields('dt'), ('id', 'ts_id', 'v'))
            sqin = "INSERT INTO ts(val) values ('bob')"
            self.assertEqual(dbm.insert(sqin), 3)
            rv1 = (('id', 'val'), [(1, 'ted'), (2, 'popi'), (3, 'bob')])
            self.assertEqual(dbm.select_table('ts', 'names-tuples'), rv1)
            sqlkv1 = "SELECT v FROM dt WHERE id=1"
            self.assertEqual(dbm.select_key_val(sqlkv1), 'Val1')
            sqlkv2 = "SELECT v FROM dt WHERE id=30"
            self.assertEqual(dbm.select_key_val(sqlkv2), None)
            ld1 = [{'id': 1, 'val': 'ted'}]
            self.assertEqual(dbm.find_records('ts', 'TE eD'), ld1)
            di2 = {'id': 2, 'val': 'popi'}
            self.assertEqual(dbm.find_record_by_id('ts', 2), [di2])
            self.assertEqual(dbm.get_zlabels(), {'id': 'ΑΑ'})

    def test_various_db_functions(self):
        dbflds = ['fld', 'id', 'lbl', 'ts_id', 'v', 'val']
        self.assertEqual(db.fields(DBTEST), dbflds)
        self.assertEqual(db.fields_of(DBTEST, 'ts'), ('id', 'val'))
        self.assertEqual(db.tables_views(DBTEST), ('dt', 'ts', 'zlbl'))
        trecs = [(1, 'ted'), (2, 'popi')]
        self.assertEqual(db.table_records(DBTEST, 'ts'), trecs)
        pragmas = {'user_version': 1963, 'app_id': 2017001}
        self.assertEqual(db.pragmas(DBTEST), pragmas)
        vals = {'id': 1, 'val': 'ted',
                'zlines': [{'id': 1, 'v': 'Val1'}, {'id': 2, 'v': 'val2'}]}
        self.assertEqual(db.find_by_id_md(DBTEST, 1, 'ts', 'dt'), vals)
        print(db.find_by_id(DBTEST, 1, 'ts', 'names-tuples'))
