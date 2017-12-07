"""
Module dates payroll.py
Managing dates for payroll purposes
"""
import calendar
import datetime as dt


class DatespayException(Exception):
    """Exceptions"""
    pass


def month_days(year, month):
    """
    :return: list with number of days per year/month
    """
    if not isinstance(year, int):
        raise DatespayException('Year must be integer')
    if not isinstance(month, int):
        raise DatespayException('Month must be integer')
    if month < 1 or month > 12:
        raise DatespayException('Month must be integer between 1 and 12')
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
    if not dateeos >= dateapo:
        raise DatespayException('dateeos must be >= to dateapo')
    flist = [0, 0, 0, 0, 0, 0, 0]
    ayear, amonth, aday = dateapo.split('-')
    eyear, emonth, eday = dateeos.split('-')
    dapo = dt.date(int(ayear), int(amonth), int(aday))
    deos = dt.date(int(eyear), int(emonth), int(eday))
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


def checkhour(tstart, duration, dur_limit=16):
    """Check hour
    :param hstart: Ώρα έναρξης σε μορφή 'hh:mm'
    :param duration: Διάρκεια σε ώρες
    :return: list with two elements : [normal_time, night_time]
    """
    night = (0, 1, 2, 3, 4, 5, 22, 23, 24, 25, 26, 27, 28, 29, 30)
    hstart, mstart = tstart.split(':')
    hstart = int(hstart)
    mstart = int(mstart) / 60.0
    if hstart > 24 or hstart < 0:
        raise DatespayException('Hour must be between 0 and 24')
    if mstart > 59 or mstart < 0:
        raise DatespayException('Minute must be between 0 and 59')
    if duration > dur_limit:
        raise DatespayException('Work time limit exceeded')
    hmend = hstart + mstart + duration
    hend = int(hmend // 1)
    mend = hmend % 1
    fval = [0, 0]
    for hour in range(hstart, hend):
        if hour in night:
            fval[1] += 1
        else:
            fval[0] += 1
    # remove from first hour decimal mstart
    if hstart in night:
        fval[1] -= mstart
    else:
        fval[0] -= mstart
    # add to last hour
    if hend in night:
        fval[1] += mend
    else:
        fval[0] += mend
    normal_hours = round(fval[0], 2)
    night_hours = round(duration - normal_hours, 2)
    return (normal_hours, night_hours)


class WeekDays:
    """Week days"""
    grdays = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη',
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

    def week_hours_di(self):
        """Κατανομή ωρών εργασίας ανα κανονικές/νυχτερινές"""
        tnormal = 0
        tnight = 0
        for day in self.ddict:
            for key in day:
                htuple = checkhour(key, day[key])
                tnormal += htuple[0]
                tnight += htuple[1]
        return (tnormal, tnight)

    def week_hours_tupl(self):
        """Return a tuple ((0, 0), (), ...)"""
        flist = []
        for day in self.ddict:
            normal = 0
            night = 0
            for key in day:
                htuple = checkhour(key, day[key])
                normal += htuple[0]
                night += htuple[1]
            flist.append((normal, night))
        return tuple(flist)

    def week_hours_analysis(self):
        """Analysis"""
        tmpl = '%-10s %-6s %6s %6s %6s\n'
        dlin = '-' * 39 + '\n'
        ast = '\nΕβδομαδιαίο πρόγραμμα εργασίας\n\n'
        ast += tmpl % ('', 'Έναρξη', 'Ημέρα', 'Νύχτα', 'Σύνολο')
        ast += dlin
        tnormal = 0.0
        tnight = 0.0
        meres_apasxolisis = 0
        for i, day in enumerate(self.ddict):
            nday = self.grdays[i]
            if day == {}:
                ast += tmpl % (nday, '', '', '', '')
            else:
                meres_apasxolisis += 1
                for key in day:
                    htu = checkhour(key, day[key])
                    fno = '%.2f' % htu[0]
                    fni = '%.2f' % htu[1]
                    fto = '%.2f' % sum(htu)
                    ast += tmpl % (nday, key, fno, fni, fto)
                    tnormal += htu[0]
                    tnight += htu[1]
        ast += dlin
        tno = '%.2f' % tnormal
        tni = '%.2f' % tnight
        tto = '%.2f' % (tnormal + tnight)
        ast += tmpl % ('Σύνολα', '', tno, tni, tto)
        ast += '\nΗμέρες εβδομαδιαίας απασχόλησης : %s\n' % meres_apasxolisis
        return ast

    def week_hours(self):
        """:return: working week hours"""
        return sum(self.dlist)

    def working_month_days(self, year, month):
        """Βρες τις εργάσιμες ημέρες του έτους/μήνα"""
        weekdays = month_days(year, month)
        for i, _ in enumerate(weekdays):
            if self.dlist[i] == 0:
                weekdays[i] = 0
        return tuple(weekdays)

    def working_days(self, dateapo, dateeos):
        """Βρες τις εργάσιμες ημέρες ανάμεσα σε δύο ημερομηνίες
        Συμπεριλαμβάνεται η αρχική και η τελική ημερομηνία
        """
        weekdays = timespace_days(dateapo, dateeos)
        for i, _ in enumerate(weekdays):
            if self.dlist[i] == 0:
                weekdays[i] = 0
        return tuple(weekdays)

    def working_days_analysis(self, dateapo, dateeos):
        """Αναλυτική εκτύπωση"""
        wdays = self.working_days(dateapo, dateeos)
        sep = '-' * 54 + '\n'
        ast = '\nΑνάλυση Ημερών εργασίας από %s έως %s\n' % (dateapo, dateeos)
        ast += '\n'
        tml = '%-10s %5s %6s %6s %7s %7s %7s\n'
        ast += tml % ('', 'ΜΕΡΕΣ', 'ΜΕΡΑ', 'ΝΥΧΤΑ', 'ΣΜΕΡΑ', 'ΣΝΥΧΤΑ',
                      'ΣΥΝΟΛΟ')
        ast += sep
        wkh = self.week_hours_tupl()
        ttme = 0
        ttny = 0
        ttda = 0
        ttto = 0
        for i, day in enumerate(wdays):
            wda = self.grdays[i]
            if day == 0:
                ast += tml % (wda, '', '', '', '', '', '')
            else:
                mer = wkh[i][0]
                nyx = wkh[i][1]
                tmer = mer * day
                tnyx = nyx * day
                ttot = tmer + tnyx
                ttme += tmer
                ttny += tnyx
                ttda += day
                ttto += ttot
                ast += tml % (wda, day, mer, nyx, tmer, tnyx, ttot)
        ast += sep
        ast += tml % ('ΣΥΝΟΛΑ', ttda, '', '', ttme, ttny, ttto)
        return ast

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


class Period():
    def __init__(self, dapo, deos):
        """
        dapo: iso date
        deos: iso date
        """
        assert dapo <= deos
        assert len(dapo) == 10
        assert len(deos) == 10
        self._apo = dt.datetime.strptime(dapo, '%Y-%m-%d')
        self._eos = dt.datetime.strptime(deos, '%Y-%m-%d')

    @property
    def days(self):
        return (self._eos - self._apo).days + 1

    @property
    def split2moths(self):
        ye1 = self._apo.year
        ye2 = self._eos.year
        mo1 = self._apo.month
        mo2 = self._eos.month


if __name__ == '__main__':
    pe1 = Period('2017-01-01', '2017-01-12')
    print(pe1.days)
    wd1 = WeekDays((0, 0, 0, 0, {'20:00': 6}, {'20:00': 6}, 0))
    print(wd1.week_hours_analysis())
    print(month_days(2017, 12))