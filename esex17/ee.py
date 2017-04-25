"""
class Esex
"""


ESODO, EKSODO, ESPAG, EKSPAG = 1, 2, 3, 4
TYPEE = {ESODO: 'Έσοδα', EKSODO: 'Έξοδα',
         ESPAG: 'Αγορές παγίων', EKSPAG: 'Πωλήσεις παγίων'}
ELLADA, ENDOK, EKSOTERIKO = 10, 20, 30
TYPXO = {ELLADA: 'Εσωτερικού', ENDOK: 'Ενδοκοινοτικό', EKSOTERIKO: 'Εξωτερικό'}


class LineType:
    """Τύπος αναλυτικής γραμμής"""
    def __init__(self, per, pfpa=0):
        self._per = per
        self._pfpa = pfpa

    def pfpa(self):
        """Μετατροπή του ΦΠΑ σε δεκαδικό"""
        return self._pfpa / 100.0

    def per(self):
        """Περιγραφή"""
        return self._per


class EsexLine:
    """Αναλυτική γραμμή εσόδων εξόδων"""
    def __init__(self, ltype, val=0, fpa=0, tot=0):
        self.line_type = ltype
        if val != 0:
            self.calc_from_val(val)
        elif fpa != 0:
            self.calc_from_fpa(fpa)
        elif tot != 0:
            self.calc_from_tot(tot)
        else:
            self._val = 0
            self._fpa = 0
            self._tot = 0

    def val(self):
        """Αξία"""
        return self._val

    def fpa(self):
        """ΦΠΑ"""
        return self._fpa

    def tot(self):
        """Συνολική αξία"""
        return self._tot

    def per(self):
        """Περιγραφή γραμμής"""
        return self.line_type.per()

    def check(self):
        """Έλεγχοι για ακεραιότητα δεδομένων"""
        if self.line_type.pfpa() == 0:
            assert self._fpa == 0
        assert self._fpa == self._val * self.line_type.pfpa()

    def calc_from_val(self, val):
        """Υπολογισμός φπα, συνόλου από αξία"""
        self._val = val
        self._fpa = self.line_type.pfpa() * val
        self._tot = self._val + self._fpa

    def calc_from_fpa(self, fpa):
        """Υπολογισμός αξίας, συνόλου από φπα"""
        self._val = fpa / self.line_type.pfpa()
        self._fpa = fpa
        self._tot = self._val + self._fpa

    def calc_from_tot(self, tot):
        """Υπολογισμός αξίας, φπα από συνολική αξία"""
        self._val = tot / (1.0 + self.line_type.pfpa())
        self._fpa = tot - self._val
        self._tot = tot


class Esex:
    """Έσοδα-έξοδα"""
    def __init__(self, dat, par, typ=ESODO, xora=ELLADA, nor=True):
        self._typ = typ  # Έσοδο ή έξοδο
        self._nor = nor  # Αν True normal διαφορετικά credit
        self._xora = xora
        self._ypma = 1  # Κεντρικό παράρτημα
        self._dat = dat  # Ημερομηνία εγγραφής
        self._par = par  # Παραστατικό
        self._lines = []
        self.tval = 0
        self.tfpa = 0
        self.ttot = 0

    def normal(self):
        if self._nor:
            return 'Normal'
        return 'Credit'

    def new_line(self, line):
        """Νέα γραμμή"""
        self._lines.append(line)
        self.tval += line.val()
        self.tfpa += line.fpa()
        self.ttot += line.tot()

    def __repr__(self):
        tmpl = '%-40s %12s %10s %13s\n'
        ast = 'Έσοδα-έξοδα\n'
        ast += '%s\n' % TYPEE[self._typ]
        for lin in self._lines:
            ast += tmpl % (lin.per(), lin.val(), lin.fpa(), lin.tot())
        ast += tmpl % ('Σύνολα', self.tval, self.tfpa, self.ttot)
        return ast


if __name__ == '__main__':
    pe24 = LineType('Πωλήσεις εμπορευμάτων 24%', 24.0)
    pe13 = LineType('Πωλήσεις εμπορευμάτων 13%', 13.0)
    ese = Esex()
    ese.new_line(EsexLine(pe24, 100))
    ese.new_line(EsexLine(pe13, 100))
    print(ese)
