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


class Per():
    def __init__(self, dapo, deos):
        self._apo = dapo
        self._eos = deos
        assert self._apo < self._eos
        assert len(self._apo) == 10
        assert len(self._eos) == 10

    def days(self):
        pass


class Period():
    def __init__(self, period='201701'):
        self._year = period[:4]
        self._month = period[4:]

        self._apo = '%s-%s-01' % (self.year, self.month)
        self._eos = '%s-%s-31' % (self.year, self.month)
        assert 0 < int(self._month) <= 12
        assert len(self._month) == 2
        assert len(self._year) == 4


    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def apo(self):
        return self._apo

    @property
    def eos(self):
        return self._eos

def calcpayroll(ptype, period, ergdata):
    """
    ptype: normal , dp, ea, dx
    """
    pass


def dikaioytai(erg, period):
    if erg.proslipsi.year < period.year:
        pass


if __name__ == "__main__":
    jan = Period('201701')
    print(jan.month, jan.year, jan.apo, jan.eos)
