"""
Module dates payroll.py
Managing dates for payroll purposes
"""
import calendar
import datetime


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


def timespace_days(dateapo, dateeos):
    """
    :param dateapo: From iso date
    :param dateeos: To iso date
    :return: list with number of days in time interval of the form:
             [Δε, Τρ, Τε, Πε, Πα, Σα, Κυ]
    """
    assert dateeos >= dateapo
    flist = [0, 0, 0, 0, 0, 0, 0]
    ayear, amonth, aday = dateapo.split('-')
    eyear, emonth, eday = dateeos.split('-')
    dapo = datetime.date(int(ayear), int(amonth), int(aday))
    deos = datetime.date(int(eyear), int(emonth), int(eday))
    # Find the first day
    first_day = dapo.weekday()
    # Find the days from first to last
    # Divide with 7 and get the rest
    delta = deos - dapo
    days = delta.days + 1
    for i in range(days):
        tday = (first_day + i) % 7
        flist[tday] += 1
    return flist


class DatespayException(Exception):
    """Exceptions"""
    pass


class WeekDays:
    """Week days"""
    grdays = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πεμπτη',
              'Παρασκευή', 'Σάββατο', 'Κυριακή']

    def __init__(self, dlist=(8, 8, 8, 8, 8, 0, 0), start='08:00'):
        """
        :param dlist: [1, 1, 1, 1, 1, 0, 0]
                      Δε,Τρ,Τε,Πε,Πα,Σα,Κυ
                      [8, 8, 8, 8, 8, 0, 0]
        Το dlist έχει 7 στοιχεία, ένα για κάθε ημέρα
        Το κάθε στοιχείο μπορεί να είναι είτε αριθμός που αντιπροσωπεύει τις
        ώρες εργασίας της ημέρας είτε dictionary με keys την ώρα έναρξης της
        εργασίας και values τις ώρες εργασίας. Σε μια ημέρα μπορεί ο
        εργαζόμενος να προσέλθει για εργασία πάνω από μια φορά.
        Άρα το dictionary μπορεί να έχει τουλάχιστον μία ή παραπάνω τιμές.
        :param start: Default hour to start working
        :return: new class
        dlist = [{'10:00': 8}, {'10:00': 8}, {'10:00': 8}, {'10:00': 8},
                 {'10:00': 8}, {'10:00': 8}, {'10:00': 8}]
        """
        if len(dlist) != 7:
            raise DatespayException('Not a proper dlist')
        self.dlist = []
        self.ddict = []
        for elm in dlist:
            if isinstance(elm, (int, float)):
                self.dlist.append(elm)
                if elm == 0:
                    self.ddict.append({})
                else:
                    self.ddict.append({start: elm})
            elif isinstance(elm, dict):
                thours = 0
                for key in elm:
                    thours += elm[key]
                self.ddict.append(elm)
                self.dlist.append(thours)
            else:
                raise DatespayException('Wrong parameter days')

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

    def working_days(self, dateapo, dateeos):
        """Βρες τις εργάσιμες ημέρες ανάμεσα σε δύο ημερομηνίες
        Συμπεριλαμβάνεται η αρχική και η τελική ημερομηνία
        """
        weekdays = timespace_days(dateapo, dateeos)
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
    """Not implemented yet"""
    def __init__(self):
        self.weekdays = 5
        self.weekhour = 40
        self.weekdaya = [1, 1, 1, 1, 1, 0, 0]
