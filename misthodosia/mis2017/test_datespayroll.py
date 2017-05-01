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

    def test_07(self):
        """Μικτή εισαγωγή δεδομένων"""
        ats = dpay.WeekDays(({}, 4, 4, 4, 4,
                             {'10:00': 2, '20:00': 4}, 0), '07:00')
        val = [{}, {'07:00': 4}, {'07:00': 4}, {'07:00': 4}, {'07:00': 4},
               {'10:00': 2, '20:00': 4}, {}]
        self.assertEqual(ats.ddict, val)
        self.assertEqual(ats.dlist, [0, 4, 4, 4, 4, 6, 0])

    def test_08(self):
        """Έλεγχος ημερήσιας/νυχτερινής ώρας"""
        self.assertEqual(dpay.checkhour('01:00', 8), (3, 5))
        self.assertEqual(dpay.checkhour('17:00', 8), (5, 3))
        self.assertEqual(dpay.checkhour('19:00', 8), (3, 5))
        self.assertEqual(dpay.checkhour('08:00', 8), (8, 0))
        self.assertEqual(dpay.checkhour('22:00', 8), (0, 8))
        self.assertEqual(dpay.checkhour('06:00', 8), (8, 0))
        self.assertEqual(dpay.checkhour('00:00', 8), (2, 6))
        self.assertEqual(dpay.checkhour('00:00', 12), (6, 6))
        self.assertEqual(dpay.checkhour('12:00', 8), (8, 0))


if __name__ == '__main__':
    unittest.main()
