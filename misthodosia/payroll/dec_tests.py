# -*- coding: utf-8 -*-

import unittest
import dec as c


class Tests_dec(unittest.TestCase):

    def test_dec(self):
        self.assertEqual(c.dec('ff'), c.dec(0))
        self.assertEqual(c.dec('3ff'), c.dec(0))
        self.assertEqual(c.dec('120.35'), c.dec(120.35))
        self.assertEqual(c.dec('120.356'), c.dec(120.36))
        self.assertEqual(c.dec('1200.24678'), c.dec(1200.25))
        self.assertEqual(c.dec('1'), c.dec(1.001))
        self.assertEqual(c.dec('0.995'), c.dec(1.004))

if __name__ == '__main__':
    unittest.main()
