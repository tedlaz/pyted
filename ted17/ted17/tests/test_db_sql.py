"""
Testing sql creation
"""
import unittest
from ted17 import db_sql as sqc

SQ1 = '''BEGIN TRANSACTION;
INSERT INTO tm (epo, ono) VALUES ('Laz', 'Ted');
INSERT INTO tmd (v, k, tm_id) VALUES ('1', '2', (SELECT MAX(id) FROM tm));
INSERT INTO tmd (v, k, tm_id) VALUES ('4', '5', (SELECT MAX(id) FROM tm));
COMMIT;'''

SQ2 = '''BEGIN TRANSACTION;
UPDATE tm SET epo='Laz', ono='Ted' WHERE id=65;
INSERT INTO tmd (v, k, tm_id) VALUES ('1', '2', '65');
INSERT INTO tmd (v, k, tm_id) VALUES ('4', '5', '65');
COMMIT;'''

SQ3 = '''BEGIN TRANSACTION;
UPDATE tm SET epo='Laz', ono='Ted' WHERE id=85;
DELETE FROM tmd WHERE id=34;
INSERT INTO tmd (v, k, tm_id) VALUES ('4', '5', '85');
UPDATE tmd SET v='8', k='9', tm_id='85' WHERE id=15;
COMMIT;'''

SQ4 = '''BEGIN TRANSACTION;
DELETE FROM tm WHERE id=10;
DELETE FROM tmd WHERE id=65;
DELETE FROM tmd WHERE id=66;
COMMIT;'''


class TestSql(unittest.TestCase):
    """Testing sql creation"""
    def test_01(self):
        """Insert transaction"""
        adic = {'epo': 'Laz', 'ono': 'Ted',
                'zlines': [{'v': 1, 'k': 2}, {'v': 4, 'k': 5}]}
        self.assertEqual(sqc.dic2sql_md('tm', 'tmd', adic), SQ1)

    def test_02(self):
        """Update transaction"""
        bdic = {'id': 65, 'epo': 'Laz', 'ono': 'Ted',
                'zlines': [{'v': 1, 'k': 2}, {'v': 4, 'k': 5}]}
        self.assertEqual(sqc.dic2sql_md('tm', 'tmd', bdic), SQ2)

    def test_03(self):
        """Mixed transaction"""
        cdic = {'id': 85, 'epo': 'Laz', 'ono': 'Ted',
                'zlines': [{'id': 34, 'v': 1, 'k': 2, '_d_': 1},
                           {'v': 4, 'k': 5}, {'id': 15, 'v': 8, 'k': 9}]}
        self.assertEqual(sqc.dic2sql_md('tm', 'tmd', cdic), SQ3)

    def test_04(self):
        """Delete transaction"""
        edic = {'id': 10, 'epo': 'Laz', 'ono': 'Ted', '_d_': 1,
                'zlines': [{'id': 65, 'v': 1, 'k': 2},
                           {'id': 66, 'v': 4, 'k': 5}]}
        self.assertEqual(sqc.dic2sql_md('tm', 'tmd', edic), SQ4)

    def test_05(self):
        """Using dic2sql insert, update, delete"""
        dic1 = {'epo': 'Lazaros', 'el_id': 34}
        sq1 = "INSERT INTO erg (epo, el_id) VALUES ('Lazaros', '34');"
        self.assertEqual(sqc.dic2sql('erg', dic1), sq1)
        dic2 = {'id': 0, 'epo': 'Lazaros', 'el_id': 34}
        sq2 = "INSERT INTO erg (epo, el_id) VALUES ('Lazaros', '34');"
        self.assertEqual(sqc.dic2sql('erg', dic2), sq2)
        dic3 = {'id': 20, 'epo': 'Lazaros', 'el_id': 34}
        sq3 = "UPDATE erg SET epo='Lazaros', el_id='34' WHERE id=20;"
        self.assertEqual(sqc.dic2sql('erg', dic3), sq3)
        dic4 = {'id': 20, 'epo': 'Lazaros', 'el_id': 34, '_d_': 1}
        sq4 = "DELETE FROM erg WHERE id=20;"
        self.assertEqual(sqc.dic2sql('erg', dic4), sq4)
