"""
Testing datespayroll.py
"""
import unittest
import datespayroll as dpay


class Tests(unittest.TestCase):
    def test_01(self):
        """Week hours"""
        pro = dpay.WeekDays()
        self.assertEqual(pro.week_hours(), 40)

    def test_02(self):
        """Test Wrong number of arguments"""
        with self.assertRaises(dpay.DatespayException):
            prot = dpay.WeekDays((4, 4, 4, 0, 0,))


if __name__ == '__main__':
    wdays = dpay.WeekDays((0, 0, 0, 0, 0, 7, 8))
    print(wdays)
    print(dpay.WeekDays())
    print(dpay.month_days(2017, 4))
    print(wdays.working_month_days(2017, 5))
    full = dpay.WeekDays()
    print(full.working_month_days(2017, 4))
