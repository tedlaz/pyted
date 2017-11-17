"""TESTING PAYROLL"""
import unittest
import payrollcalc as pc
import utils as ul


class TestPayroll(unittest.TestCase):

    def test_normal(self):
        n01 = {'typ': 'misthos', 'apo': 600, 'meres': 25}
        self.assertEqual(pc.normal(n01)[0]['apop'], 600)
        n01 = {'typ': 'imeromisthio', 'apo': 30, 'meres': 25}
        self.assertEqual(pc.normal(n01)[0]['apop'], 750)
        n01 = {'typ': 'oromisthio', 'apo': 5, 'ores': 100}
        self.assertEqual(pc.normal(n01)[0]['apop'], 500)
        n01 = {'typ': 'misthos', 'apo': 3200, 'apon': 2400, 'meres': 1,
               'argiao': 5, 'nyxtao': 7}
        res, _ = pc.normal(n01)
        self.assertEqual(res['apop'], 128)
        self.assertEqual(res['apoao'], 54)
        self.assertEqual(res['apodn'], ul.dec(25.2))
        self.assertEqual(res['apot'], ul.dec(207.20))

    def test_yperories(self):
        nyp = {'oro': 19.2, 'oron': 14.4, 'ype': 4, 'ypen': 1, 'ypea': 4}
        res, _ = pc.yperories(nyp)
        self.assertEqual(res['ayp'], ul.dec(76.8))
        self.assertEqual(res['aypa'], ul.dec(43.2))
        self.assertEqual(res['aypn'], ul.dec(3.6))
        self.assertEqual(res['aypp'], ul.dec(61.8))
        self.assertEqual(res['aypt'], ul.dec(185.4))

    def test_astheneia(self):
        pass

    def test_ika(self):
        pass

    def test_doro_pasxa(self):
        pass

    def test_doro_xristoygennon(self):
        pass

    def test_epidoma_adeias(self):
        dea01 = {'typ': 'misthos', 'merest': 25, 'apo': 600}
        self.assertEqual(pc.epidoma_adeias(dea01)[0]['aea'], 48)
