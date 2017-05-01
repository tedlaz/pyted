"""
Testing datespayroll.py
"""
import unittest
import datespayroll as dpay


class Tests(unittest.TestCase):
    """Main testing"""
    def test_01(self):
        """Week hours"""
        pro = dpay.WeekDays()
        self.assertEqual(pro.week_hours(), 40)

    def test_02(self):
        """Test Wrong number of arguments"""
        with self.assertRaises(dpay.DatespayException):
            _ = dpay.WeekDays((4, 4, 4, 0, 0,))

    def test_03(self):
        """timespace_dates"""
        daylist = dpay.timespace_days('2017-04-18', '2017-04-30')
        self.assertEqual(daylist, [1, 2, 2, 2, 2, 2, 2])

    def test_04(self):
        """month_days"""
        self.assertEqual(dpay.month_days(2017, 4), [4, 4, 4, 4, 4, 5, 5])

    def test_05(self):
        """Full employment"""
        full = dpay.WeekDays()
        self.assertEqual(full.working_month_days(2017, 4), 20)
        self.assertEqual(full.working_days('2017-04-18', '2017-04-30'), 9)

    def test_06(self):
        """Μερική απασχόληση"""
        wdays = dpay.WeekDays((0, 4, 4, 4, 4, 4, 0))
        self.assertEqual(wdays.working_month_days(2017, 5), 22)
