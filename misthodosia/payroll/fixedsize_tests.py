# -*- coding: utf-8 -*-

import unittest
import fixedsize as c


class Tests_fixedsize(unittest.TestCase):

    def test_fmt(self):
        self.assertEqual(c.fmt(12, 'i10'), '0000000012')
        self.assertEqual(c.fmt(12, 'n10'), '0000001200')
        self.assertEqual(c.fmt(12, 'd10'), '        12')
        self.assertEqual(c.fmt(12, 'x10'), '12        ')

    def test_defmt(self):
        self.assertEqual(c.defmt('12', 'i'), 12)
        self.assertEqual(c.defmt('1200', 'n'), c.dec(12))
        self.assertEqual(c.defmt('12   ', 'd'), '12')
        self.assertEqual(c.defmt('     12   ', 'x'), '12')


if __name__ == '__main__':
    unittest.main()
