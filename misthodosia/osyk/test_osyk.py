# -*- coding: utf-8 -*-
"""Module test_osyk.py"""
import unittest
import osyk as ok


class TestsOsyk(unittest.TestCase):
    """Test cases"""

    def test_split_strip(self):
        self.assertEqual(ok.split_strip('ep|on|pat'), ['ep', 'on', 'pat'])

    def test_eid_find(self):
        self.assertEqual(ok.eid_find('913230'), ('913230', u'Λαντζέρης'))
        self.assertEqual(ok.eid_find('9132301'), None)

    def test_kad_find(self):
        self.assertEqual(ok.kad_find('5540'), ('5540', u'Μπάρ'))
        self.assertEqual(ok.kad_find('55403'), None)

    def test_kad_list(self):
        self.assertEqual(ok.kad_list('55403'), [])
        self.assertEqual(ok.kad_list('aas'), [])

    def test_eid_kad_list(self):
        self.assertEqual(ok.kad_list('55403'), [])

    def test_kpk_find(self):
        r = ('103', u'ΜΙΚΤΑ', '12.5000', '21.5600', '34.0600', '201407')
        self.assertEqual(ok.kpk_find('103', '201410'), r)
        r1 = ('101', u'ΜΙΚΤΑ, ΙΚΑ-ΤΕΑΜ', '15.5000', '24.5600', '40.0600', '201407')
        self.assertEqual(ok.kpk_find('101', '201605'), r1)
        r2 = ('101', u'ΜΙΚΤΑ, ΙΚΑ-ΤΕΑΜ', '16.0000', '25.0600', '41.0600', '201606')
        self.assertEqual(ok.kpk_find('101', '201606'), r2)

    def test_kadeidkpk_find(self):
        pass


if __name__ == '__main__':
    unittest.main()
