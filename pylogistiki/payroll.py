"""Greek payroll system
έχουμε τα εξής

 dateFrom    dateTo     ergAMKA   meres argia nyxta
Normal
2017-01-01 2017-01-31 12345678901  10    0     3
2017-01-01 2017-01-31 33333333333   5    0     0

Astheneia
2017-01-10 2017-01-14 12345678901   2    3     120

yperoria
2017-01-10 2017-01-14 12345678901   12

Το σύστημα συγκεντρώνει από τρείς πίνακες τα δεδομένα με βάση την ημερομηνία
και κάνει τον υπολογισμό.

jan2017 = 2017-01-01 2017-01-31
calcmis_per(jan2017) :
    για κάθε τύπο παρουσίας υπολόγισε τις αποδοχές
    υπολόγισε το ικα
    υπολόγισε τους φόρους
    υπολόγισε το καθαρό
    συγκέντρωσε τα ποσά
    Για κάθε εργαζόμενο
    πρέπει να υπολογίζεται τουλάχιστον πέρα από τις κανονικές περιόδους,
    δώρο πάσχα ή και χριστουγέννων, επίδομα αδείας
    apo1  eos1
    apo2  eos2

    apo1 < eos1
    apo1 < apo2
    apo1 < eos2
    apo1 > apo2
    apo1 > eos2

    ----------------apo1-------------------eos1-----------------
    --apo2----eos2----------------------------------------------
    --apo2----------eos2----------------------------------------
    --apo2--------------------eos2------------------------------
    --apo2---------------------------------eos2-----------------
    --apo2----------------------------------------------eos2----
    ----------------apo2-------------------eos2-----------------
    ----------------------apo2----eos2--------------------------
    --------------------------apo2----------------------eos2----
    ---------------------------------------------apo2---eos2----
          |-----------|
     |--|                      ανεξάρτητα
     |----|                    διαδοχικά
     |----------|              επικαλυπτόμενα
     |----------------|        επ2
     |---------------------|   περιεχόμενα
          |-----|              περιεχομενα 2
          |-----------|        ΙΣΑ!!!!!!!!
          |----------------|   επ2
                |--|           περιεχόμενα
                |-----|        περιεχόμενα 2
                |----------|   επικαλυπτόμενα
                      |----|   διαδοχικά
                        |--|   ανεξάρτητα
"""
import datetime as dt
import calendar
from utils import grup


class Period():
    def __init__(self, tapo, teos):
        """
        dapo: iso date
        deos: iso date
        """
        assert tapo <= teos
        assert len(tapo) == 10
        assert len(teos) == 10
        self._apo = tapo
        self._eos = teos

    @property
    def dapo(self):
        '''Returns datetime object'''
        return dt.datetime.strptime(self._apo, '%Y-%m-%d')

    @property
    def deos(self):
        '''Returns datetime object'''
        return dt.datetime.strptime(self._eos, '%Y-%m-%d')

    @property
    def days(self):
        '''Returns difference in days'''
        return (self.deos - self.dapo).days + 1

    @property
    def split2moths(self):
        '''Split a period to periods per month'''
        ye1 = self.dapo.year
        ye2 = self.deos.year
        mo1 = self.dapo.month
        mo2 = self.deos.month
        yeardiff = ye2 - ye1
        fmo2 = mo2 + (yeardiff * 12)
        monthdiff = fmo2 - mo1 + 1
        pers = []
        yea = ye1
        mon = mo1
        for i in range(monthdiff):

            pers.append((yea, mon, calendar.monthrange(yea, mon)))
            mon += 1
            if mon > 12:
                mon = 1
                yea += 1
        return monthdiff, pers

    def __str__(self):
        return '%s:%s' % (self._apo, self._eos)


def calcpayroll(ptype, period, ergdata):
    """
    ptype: normal , dp, ea, dx
    """
    pass


def dikaioytai(erg, period):
    if erg.proslipsi.year < period.year:
        pass


class apoysies():
    def __init__(self, aps):
        self._apo = aps['apo']
        self._eos = aps['eos']
        self._erg = aps['erg']
        self._typ = aps['typ']  # astheneia, adeia, adikaiologiti apousia klp

    def working_days(self):
        return 1

    def tst(self):
        if self._typ == 'astheneia':
            pass


if __name__ == "__main__":
    # erg = Erg()
    # erg.status()
    # erg.type()
    # erg.proslipsi
    # erg.apoxorisi
    # erg['apoxorisi']
    # erg.epo
    # erg.ono
    # erg.afm
    epo = 'πόπη Δαζέα kai loipa'
    print(epo, grup(epo))
    siv = ['epo', 'ono', 'pat']
    ggg = {'epo': 'a', 'ono': 'b', 'pat': 'c'}
    # assert required(siv, ggg)
    pe1 = Period('2015-12-28', '2017-03-01')
    print(pe1.days)
    print(pe1.split2moths)
    print(pe1)