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
        nas = {'isthio': 80, 'ml3': 3, 'mm3': 6, 'epi': 350}
        res, _ = pc.astheneia(nas)
        self.assertEqual(res['asl3'], ul.dec(120))
        self.assertEqual(res['asm3'], ul.dec(480))
        self.assertEqual(res['asti'], ul.dec(600))
        self.assertEqual(res['axe'], ul.dec(250))

    def test_ika(self):
        nik = {'poso': 100, 'pika': .45, 'pikae': .15}
        self.assertEqual(pc.ika(nik)[0]['ika'], ul.dec(45))
        nik = {'poso': 100, 'pika': 45, 'pikae': 15}
        self.assertEqual(pc.ika(nik)[0]['ika'], ul.dec(45))

    def test_doro_pasxa(self):
        ndp = {'typ': 'misthos', 'merest': 25, 'apo': 600}
        self.assertEqual(pc.doro_pasxa(ndp)[0]['dpas'], ul.dec(78.13))
        ndp = {'typ': 'misthos', 'merest': 500, 'apo': 600}
        self.assertEqual(pc.doro_pasxa(ndp)[0]['dpas'], ul.dec(312.5))
        ndp = {'typ': 'imeromisthio', 'merest': 25, 'apo': 30}
        self.assertEqual(pc.doro_pasxa(ndp)[0]['dpas'], ul.dec(120.19))
        ndp = {'typ': 'imeromisthio', 'merest': 500, 'apo': 30}
        self.assertEqual(pc.doro_pasxa(ndp)[0]['dpas'], ul.dec(468.75))
        ndp = {'typ': 'oromisthio', 'apo': 600}
        self.assertEqual(pc.doro_pasxa(ndp)[0]['dpas'], ul.dec(78.13))

    def test_doro_xristoygennon(self):
        ndx = {'typ': 'misthos', 'merest': 25, 'apo': 600}
        self.assertEqual(pc.doro_xrist(ndx)[0]['dxri'], ul.dec(78.13))
        ndx = {'typ': 'misthos', 'merest': 500, 'apo': 600}
        self.assertEqual(pc.doro_xrist(ndx)[0]['dxri'], ul.dec(625))
        ndx = {'typ': 'imeromisthio', 'merest': 25, 'apo': 30}
        self.assertEqual(pc.doro_xrist(ndx)[0]['dxri'], ul.dec(97.66))
        ndx = {'typ': 'imeromisthio', 'merest': 500, 'apo': 30}
        self.assertEqual(pc.doro_xrist(ndx)[0]['dxri'], ul.dec(781.25))
        ndx = {'typ': 'oromisthio', 'apo': 600}
        self.assertEqual(pc.doro_xrist(ndx)[0]['dxri'], ul.dec(78.13))

    def test_epidoma_adeias(self):
        dea01 = {'typ': 'misthos', 'merest': 25, 'apo': 600}
        self.assertEqual(pc.epidoma_adeias(dea01)[0]['aea'], 48)
