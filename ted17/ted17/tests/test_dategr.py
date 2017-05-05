"""Module test_dategr"""
import unittest
from ted17 import dategr as dt


class Tests(unittest.TestCase):
    """Tests"""
    def test_date2gr(self):
        self.assertEqual(dt.date2gr('2016-10-01'), '01/10/2016')
        self.assertEqual(dt.date2gr('2016-11-01', True), '1/11/2016')
        self.assertEqual(dt.date2gr('2016-05-07', True), '7/5/2016')

    def test_grdate2iso(self):
        self.assertEqual(dt.grdate2iso('1/5/2017'), '2017-05-01')

    def test_getymd_from_iso(self):
        year, month, day = dt.getymd_from_iso('2017-11-07')
        self.assertEqual([year, month, day], [2017, 11, 7])

    def test_saizon(self):
        self.assertEqual(dt.saizon('2017-01-01', 9), '2016-2017(9)')

    def test_week(self):
        self.assertEqual(dt.week('2016-01-09'), '2016w01')

    def test_period(self):
        isod = '2017-07-08'
        self.assertEqual(dt.period(isod, 2), '2017-4οΔίμ')
        self.assertEqual(dt.period(isod, 3), '2017-3οΤρίμ')
        self.assertEqual(dt.period(isod, 4), '2017-2οΤετρ')
        self.assertEqual(dt.period(isod, 6), '2017-2οΕξάμ')

    def test_group_selector(self):
        isod = '2017-07-08'
        self.assertEqual(dt.group_selector(isod, 'd'), isod)
        self.assertEqual(dt.group_selector(isod, 'm'), '2017-07')
        self.assertEqual(dt.group_selector(isod, 'y'), '2017')
        self.assertEqual(dt.group_selector(isod, 'm2'), '2017-4οΔίμ')
        self.assertEqual(dt.group_selector(isod, 'm3'), '2017-3οΤρίμ')
        self.assertEqual(dt.group_selector(isod, 'm4'), '2017-2οΤετρ')
        self.assertEqual(dt.group_selector(isod, 'm6'), '2017-2οΕξάμ')
        self.assertEqual(dt.group_selector(isod, 'w'), '2017w27')
        self.assertEqual(dt.group_selector(isod, 's'), '2016-2017(10)')
        self.assertEqual(dt.group_selector(isod, 'bullsheet'), '2017')
