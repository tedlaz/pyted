"""
symbasi.py : Κλάση που αντιπροσωπεύει τη Σύμβαση εργασίας
Λούτσα 16 Απριλίου 2017 ανήμερα Πάσχα
"""


class Symbasi_exception(Exception):
    pass

PROS_NYXTA = 0.25
PROS_ARGIA = 0.75
IKA_DAYS_WEEK = 6.0
PENTHIMERO = 5.0
EJAIMERO = 6.0
IKA_DAYS_MONTH_MISTHOTOS = 25.0
IKA_DAYS_MONTH_IMEROMIST = 26.0
IKA_HOURS_WEEK = 40.0
IKA_MISTHOS = 586.08
IKA_WEEK_TO_MONTH = round(IKA_DAYS_MONTH_IMEROMIST / EJAIMERO, 3)
IKA_IMEROMISTHIO_MISTHOTOY = round(IKA_MISTHOS / IKA_DAYS_MONTH_MISTHOTOS, 2)
IKA_IMEROMISTHIO = 26.18
IKA_OROMISTHIO = round(IKA_IMEROMISTHIO * EJAIMERO / IKA_HOURS_WEEK, 2)
MISTHOS, IMEROMISTHIO, OROMISTHIO = range(3)
ATYPOS = {0: 'Μισθωτός', 1: 'Ημερομίσθιος', 2: 'Ωρομίσθιος'}
AORISTOY, ORISMENOY, ERGOY = range(3)
STYPOS = {0: 'Αορίστου Χρόνου', 1: 'Ορισμένου Χρόνου', 2: 'Εργου'}


class Symbasi:
    """Σύμβαση εργασίας"""
    def __init__(self,
                 stypos,
                 typos,
                 apod,
                 wdays=PENTHIMERO,
                 wores=IKA_HOURS_WEEK,
                 mdays=IKA_DAYS_MONTH_MISTHOTOS):
        """
        stypos: Typos symbasis (Aoristoy xronoy, Orismenoy, Ergoy)
        typos : Misthotos, imeromisthios, oromisthios
        apod  : Apodoxes (misthos, imeromisthio, oromisthio)
        wdays : Working days per week
        whour : Working hours per week
        """
        self.stypos = stypos
        self.typos = typos
        self.apod = apod
        self.mdays = mdays
        self.wdays = wdays
        self.mdays = mdays
        self.wores = wores
        self.dores = round(self.wores / self.wdays, 3)
        if typos == MISTHOS:
            self.misthos = apod
            self.imeromisthio = apod / self.wdays
            self.oromisthio = self.imeromisthio * self.wdays / self.wores
        elif typos == IMEROMISTHIO:
            self.imeromisthio = apod
            self.oromisthio = self.imeromisthio * self.wdays / self.wores
        elif typos == OROMISTHIO:
            self.oromisthio = apod
        else:
            raise Symbasi_exception('Impossible typos')

    def check(self):
        """Έλεγχος με βάση τη Γενική συλλογική σύμβαση"""
        if self.typos == MISTHOS:
            if self.imeromisthio < IKA_IMEROMISTHIO_MISTHOTOY:
                raise Symbasi_exception('Μισθός κάτω από τον προβλεπόμενο')
        elif self.typos == IMEROMISTHIO:
            if self.imeromisthio < IKA_IMEROMISTHIO:
                raise Symbasi_exception('Ημερομίσθιο κάτω από το προβλεπόμενο')
        elif self.typos == OROMISTHIO:
            if self.oromisthio < IKA_OROMISTHIO:
                raise Symbasi_exception('Ωρομίσθιο κάτω από το προβλεπόμενο')

    def atypos(self):
        """Τύπος σύμβασης"""
        return ATYPOS[self.typos]

    def diarkeia(self):
        """Διάρκεια σύμβασης"""
        return STYPOS[self.stypos]

    def calc_nyxterina(self, ores):
        """Προσαύξηση νυχτερινών ωρών εργασίας"""
        return round(self.oromisthio * PROS_NYXTA * ores, 2)

    def calc_argia_meres(self, meres):
        """Προσαύξηση Ημερών Κυριακών/ Αργιών"""
        return round(self.imeromisthio * PROS_ARGIA * meres, 2)

    def calc_argia_ores(self, ores):
        """Προσαύξηση Ωρών Κυριακών/Αργιών"""
        return round(self.oromisthio * PROS_ARGIA * ores, 2)

    def calc_apod(self, meres, ores=0):
        """Υπολογισμός αποδοχών περιόδου"""
        if self.typos == MISTHOS:
            return self.misthos * meres / self.mdays
        elif self.typos == IMEROMISTHIO:
            return self.imeromisthio * meres
        elif self.typos == OROMISTHIO:
            return self.oromisthio * ores
        else:
            raise Symbasi_exception('Impossible type')

    def __repr__(self):
        ast = "Σύμβαση εργασίας %s\n" % self.diarkeia()
        ast += "Τύπος              : %s\n" % self.atypos()
        ast += "Αποδοχές           : %s\n" % self.apod
        ast += "Ημέρες ανά βδομάδα : %s\n" % self.wdays
        ast += "Ώρες ανά βδομάδα   : %s\n" % self.wores
        ast += "Ώρες ανά ημέρα     : %s\n" % self.dores
        return ast

if __name__ == "__main__":
    sym1 = Symbasi(AORISTOY, MISTHOS, 344.52)
    print(sym1)
    sym2 = Symbasi(AORISTOY, IMEROMISTHIO, 26.17)
    print(sym2)
    print(sym2.calc_apod(10))
    sym2.check()
