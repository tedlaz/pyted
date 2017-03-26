import sys
import os
import unittest

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if PATH not in sys.path:
    sys.path.append(PATH)

import db.sqlite as tsql


class TestGeneric(unittest.TestCase):

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

    def test_one(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
