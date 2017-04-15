# -*- coding: utf-8 -*-
from tedutil_old import ted_sqlite as tsql
import unittest
import os


class Ted_sqlite_tests(unittest.TestCase):

    def setUp(self):
        # Initialize data
        sql1 = "CREATE TABLE tst (id INTEGER PRIMARY KEY, epo TEXT);"
        self.select = 'SELECT * FROM tst'
        self.fname = 'tst.sql3'
        self.backup = 'tstbackup.sql'
        tsql.script_on_new_db(self.fname, sql1)

    def tearDown(self):
        # Clean up finally
        os.remove(self.fname)
        if os.path.exists(self.backup):
            os.remove(self.backup)

    def test_select(self):
        a = tsql.select_field_names(self.fname, self.select)
        self.assertEqual(a, ['id', 'epo'])

    def test_select_with_functions(self):
        sq1 = "INSErt into tst values(2, 'ted');"
        tsql.insert(self.fname, sq1)
        sql2 = "select grup(epo) from tst"
        v = tsql.select_with_functions(self.fname, sql2)
        self.assertEqual(v[0][0], u'TED')

    def test_insert(self):
        sq1 = "INSErt into tst values(2, 'ted');"
        self.assertEqual(tsql.insert(self.fname, sq1), 2)
        v = tsql.select(self.fname, self.select)
        tsql.backup(self.fname, self.backup)
        self.assertEqual(v[0][0], 2)
        self.assertEqual(v[0][1], u'ted')


if __name__ == '__main__':
    unittest.main()
