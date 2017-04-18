"""
Testing module
"""
import unittest
import symbasi as sm


class TestSymbasiMisthotos(unittest.TestCase):
    """Tests"""
    def setUp(self):
        self.sym = sm.Symbasi(sm.AORISTOY, sm.MISTHOS, 750.0)

    def test_atypos(self):
        self.assertEqual(self.sym.atypos(), 'Μισθωτός')

    def test_diarkeia(self):
        self.assertEqual(self.sym.diarkeia(), 'Αορίστου Χρόνου')

    def test_calc_nyxterina(self):
        self.assertEqual(self.sym.calc_nyxterina(5), 4.69)

    def test_imeromisthio(self):
        self.assertEqual(self.sym.imeromisthio, 30.00)


if __name__ == "__main__":
    SYM1 = sm.Symbasi(sm.AORISTOY, sm.MISTHOS, 344.52)
    print(SYM1)
    SYM2 = sm.Symbasi(sm.AORISTOY, sm.IMEROMISTHIO, 26.18, 3, 19)
    print(SYM2)
    print(SYM2.calc_apod(10))
    SYM2.check()
    print(SYM2.calc_misthos(40))
