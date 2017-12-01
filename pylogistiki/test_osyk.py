"""TESTING utils.py"""
import unittest
import osyk as osk


class TestOsyk(unittest.TestCase):

    def test_dec(self):
        osyk = osk.Osyk()
        per1 = 201606
        kad1 = 1120
        eid1 = 411410
        # print(osyk._kad)
        # print(osyk.find_kad('5540'))
        # print(osyk.find_eid('724070'))
        # print(osyk._kadi['5540'])
        # print(osyk._kpk)
        kpk1 = osyk.find_kpk_periodou(kad1, eid1, per1)
        kpka = osyk.find_kpk_pososta(kpk1['kpk'], per1)
        # print(kpk1, kpka)
        # pprint(osyk.find_kad('5540'))
        osk.pprint(osyk.find_kad_eids('5540', 201605))
        # print(osyk._kek)