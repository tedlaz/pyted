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

    def test_month_days(self):
        self.assertEqual(dpay.month_days(2017, 4), [4, 4, 4, 4, 4, 5, 5])


if __name__ == '__main__':
    wdays = dpay.WeekDays((0, 4, 4, 4, 4, 4, 0))
    print(wdays)
    print(wdays.working_month_days(2017, 5))
    full = dpay.WeekDays()
    print(full.working_month_days(2017, 4))
    print(full.working_days_between('2017-04-18', '2017-04-30'))
    print(dpay.month_days(2017, 4))
    print(dpay.timespace_days('2017-04-18', '2017-04-30'))
