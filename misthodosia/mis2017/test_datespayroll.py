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
        rli = (4, 4, 4, 4, 4, 0, 0)
        self.assertEqual(full.working_month_days(2017, 4), rli)
        rli = (1, 2, 2, 2, 2, 0, 0)
        self.assertEqual(full.working_days('2017-04-18', '2017-04-30'), rli)

    def test_06(self):
        """Μερική απασχόληση"""
        wdays = dpay.WeekDays((0, 4, 4, 4, 4, 4, 0))
        rli = (0, 5, 5, 4, 4, 4, 0)
        self.assertEqual(wdays.working_month_days(2017, 5), rli)

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
        self.assertEqual(dpay.checkhour('01:30', 8), (3.5, 4.5))
        self.assertEqual(dpay.checkhour('17:00', 8), (5, 3))
        self.assertEqual(dpay.checkhour('19:00', 8), (3, 5))
        self.assertEqual(dpay.checkhour('08:00', 8), (8, 0))
        self.assertEqual(dpay.checkhour('22:00', 8), (0, 8))
        self.assertEqual(dpay.checkhour('06:00', 8), (8, 0))
        self.assertEqual(dpay.checkhour('00:00', 8), (2, 6))
        self.assertEqual(dpay.checkhour('00:30', 12), (6.5, 5.5))
        self.assertEqual(dpay.checkhour('12:00', 8), (8, 0))


if __name__ == '__main__':
    print(dpay.checkhour('14:15', 8))
    ful = dpay.WeekDays(({'14:15': 8}, {'15:30': 8}, {'16:00': 8}, {'15:15': 8},
                         {'22:00': 8}, {}, {}))
    fu2 = dpay.WeekDays(({}, {'10:00': 4}, {'10:00': 2, '22:00': 2}, {'10:00': 4},
                         {'21:00': 4}, {'21:00': 4}, {}))
    print(ful.week_hours_di())
    print(ful.week_hours_tupl())
    print(fu2.week_hours_analysis())
    print(fu2.working_month_days(2017, 5))
    print(fu2.working_days('2017-04-07', '2017-04-30'))
    print(fu2.working_days_analysis('2017-05-01', '2017-05-31'))
    unittest.main()
