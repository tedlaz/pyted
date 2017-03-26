# -*- coding: utf-8 -*-
import unittest
from pymiles.utils import txt_num as tn


class Dbtests(unittest.TestCase):

    def setUp(self):
        # Initialize data
        pass

    def tearDown(self):
        # Clean up finally
        pass

    def test_equal_strGrDec(self):
        txtnum = tn.strGrDec('-123456789123456789.34')
        self.assertEqual(txtnum, '-123.456.789.123.456.789,34')

    def test_equal_strGrToDec(self):
        self.assertEqual(tn.strGrToDec('-120.345,24'), tn.dec(-120345.24))

    def test_equal_round(self):
        self.assertEqual(tn.dec('1.3451'), tn.dec(1.35))

    def test_equal_nul2DecimalZero(self):
        num = tn.nul2DecimalZero('')
        self.assertEqual(num, 0)

    def test_equal_nul2DecimalZero2(self):
        self.assertEqual(tn.dec(), 0)

    def test_equal_distribute(self):
        distlist = tn.distribute(620.35, [204, 159, 243, 120, 274])
        vlist = [tn.dec(126.55), tn.dec(98.64), tn.dec(150.75),
                 tn.dec(74.44), tn.dec('169.97')]
        self.assertEqual(distlist, vlist)
        self.assertEqual(sum(distlist), tn.dec(620.35))

    def test_Ddict(self):
        decdic = tn.Ddict(ted=100, popi=34)
        decdic['val'] = 10.235
        td = {'ted': tn.dec(100), 'popi': tn.dec(34), 'val': tn.dec(10.24)}
        self.assertEqual(decdic, td)

    def test_Ddict_not_numeric_values(self):
        decdic = tn.Ddict(ted=100, popi='tst')
        td = {'ted': tn.dec(100), 'popi': tn.dec(0)}
        self.assertEqual(decdic, td)

if __name__ == '__main__':
    unittest.main()
