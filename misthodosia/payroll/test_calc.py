# -*- coding: utf-8 -*-

import unittest
import calc as c


class Tests(unittest.TestCase):

    def test_doro_xrist(self):
        self.assertEqual(c.dec('520.83'), c.doro_xrist(250, 500, True))
        self.assertEqual(c.dec('26.04'), c.doro_xrist(8, 25, False))

    def test_doro_pasxa(self):
        self.assertEqual(c.dec('217.01'), c.doro_pasxa(100, 500, True))
        self.assertEqual(c.dec('32.05'), c.doro_pasxa(8, 25, False))

        self.assertEqual(c.dec('260.42'), c.doro_pasxa(500, 500, True))
        self.assertEqual(c.dec('390.62'), c.doro_pasxa(500, 25, False))

    def test_mines_misthoton(self):
        self.assertEqual(c.mines_misthoton(0), 0)
        self.assertEqual(c.mines_misthoton(1), 2)
        self.assertEqual(c.mines_misthoton(8), 5)

    def test_meres_imeromisthion(self):
        self.assertEqual(c.meres_imeromisthion(0), 0)
        self.assertEqual(c.meres_imeromisthion(1), 7)

    def test_apoz_apol(self):
        self.assertEqual(c.dec('0'), c.apoz_apol(.8, 1000, True))
        self.assertEqual(c.dec('2333.33'), c.apoz_apol(1, 1000, True))
        self.assertEqual(c.dec('12833.33'), c.apoz_apol(15, 1000, True))
        self.assertEqual(c.dec('28000'), c.apoz_apol(28, 1000, True))
        self.assertEqual(c.dec('28000'), c.apoz_apol(31, 1000, True))
        self.assertEqual(c.dec('8750'), c.apoz_apol(9, 1500, True))
        self.assertEqual(c.dec('14000'), c.apoz_apol(31, 1000, True, True))

        self.assertEqual(c.dec('0'), c.apoz_apol(.9, 30.32, False))
        self.assertEqual(c.dec('3537.33'), c.apoz_apol(15, 30.32, False))
        self.assertEqual(c.dec('5836.6'), c.apoz_apol(30, 30.32, False))
        self.assertEqual(c.dec('5836.6'), c.apoz_apol(35, 30.32, False))
        self.assertEqual(c.dec('2918.3'), c.apoz_apol(35, 30.32, False, True))

    def test_epidoma_adeias(self):
        self.assertEqual(c.dec('480'), c.epidoma_adeias(150, 1000, True))
        self.assertEqual(c.dec('54'), c.epidoma_adeias(15, 45, False))

    def test_foros_eisodimatos(self):
        self.assertEqual(c.dec(1411.62), c.foros_eis(15052.8, 0 , True))
        self.assertEqual(c.dec(1390.45), c.foros_eispar(15052.8, 0 , True))


if __name__ == '__main__':
    unittest.main()
