"""Πάγια
"""
import utils as ul
import datetime as dt


class Lmos():
    def __init__(self, code, per, synt):
        self.code = code
        self.per = per
        self.synt = ul.dec(synt)
        assert synt >= 0
        if self.synt != 0:
            if self.synt > 1:
                self.synt = ul.dec(self.synt / ul.dec(100))


class Pagio():
    def __init__(self, lmos, per, date, par, prom, ajia, tem=1):
        self.lmos = lmos  # Λογαριασμός λογιστικής
        self.per = per  # Περιγραφή παγίου
        self.date = date  # Ημερομηνία κτήσης
        self.par = par  # Παραστατικό αγοράς
        self.prom = prom  # Προμηθευτής
        self.ajia = ul.dec(ajia)  # Αξία
        self.tem = int(tem)  # Τεμάχια

    def calc_etisia_aposbesi(self):
        return ul.dec(self.ajia * self.lmos.synt)

    def calc_aposbesi_periodoy(self, apo, eos):
        ayear, amonth, aday = apo.split('-')
        eyear, emonth, eday = eos.split('-')
        ayear = int(ayear)
        eyear = int(eyear)
        dapo = dt.date(ayear, int(amonth), int(aday))
        deos = dt.date(eyear, int(emonth), int(eday))
        meres = ul.dec((deos - dapo).days + 1)
        yadays = (dt.date(ayear, 12, 31) - dt.date(ayear, 1, 1)).days + 1
        yedays = (dt.date(eyear, 12, 31) - dt.date(eyear, 1, 1)).days + 1
        pmeres = meres / ul.dec(max(yadays, yedays))
        return ul.dec(self.calc_etisia_aposbesi() * pmeres)


class Aposbeseis():
    def __init__(self):
        pass


if __name__ == '__main__':
    comp = Lmos('14.00', 'Υπολογιστές', 20)
    pa1 = Pagio(comp, 'Υπολογιστής', '2018-01-12', 'ΤΙΜ34', 'Λάζαρος', 100)
    print(pa1.calc_etisia_aposbesi())
    print(pa1.calc_aposbesi_periodoy('2016-01-01', '2016-01-31'))
