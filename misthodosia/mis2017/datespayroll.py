"""
Module dates payroll.py
Managing dates for payroll purposes
"""
import calendar


def month_days(year, month):
    """
    :return: list with number of days per year/month
    """
    alst = calendar.monthcalendar(year, month)
    weekdays = [0, 0, 0, 0, 0, 0, 0]
    for week in alst:
        for i, day in enumerate(week):
            if day > 0:
                weekdays[i] += 1
    return weekdays


class DatespayException(Exception):
    pass


class WeekDays:
    """Week days"""
    grdays = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πεμπτη',
              'Παρασκευή', 'Σάββατο', 'Κυριακή']

    def __init__(self, dlist=(8, 8, 8, 8, 8, 0, 0)):
        """
        :param dlist: [1, 1, 1, 1, 1, 0, 0]
                       Δ,Τρ,Τε,Πε,Πα,Σα,Κυ
                       [8, 8, 8, 8, 8, 0, 0]
        :return: new class
        """
        if len(dlist) != 7:
            raise DatespayException('Not a proper dlist')
        self.dlist = dlist

    def week_hours(self):
        """:return: working week hours"""
        return sum(self.dlist)

    def working_month_days(self, year, month):
        """Βρες τις εργάσιμες ημέρες του έτους/μήνα"""
        weekdays = month_days(year, month)
        for i, _ in enumerate(weekdays):
            if self.dlist[i] == 0:
                weekdays[i] = 0
        return sum(weekdays)

    def __repr__(self):
        sep = '-' * 32 + '\n'
        ast = 'Ημέρες εργασίας ανά βδομάδα :%3s\n'
        ast += sep
        tmpl = '%-10s : %3s ώρες\n'
        tdays = 0  # Ημέρες εργασίας ανά βδομάδα
        for i, ores in enumerate(self.dlist):
            if ores > 0:
                tdays += 1
                ast += tmpl % (self.grdays[i], ores)
        ast += sep
        ast += tmpl % ('Σύνολο', self.week_hours())
        return ast % tdays


class Programa:
    def __init__(self, tst):
        self.weekdays = 5
        self.weekhour = 40
        self.weekdaya = [1, 1, 1, 1, 1, 0, 0]
