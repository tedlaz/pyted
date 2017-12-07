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
from utils import grup, required


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
    assert required(siv, ggg)
    pe1 = Period('2016-02-28', '2016-03-01')
    print(pe1.days)
