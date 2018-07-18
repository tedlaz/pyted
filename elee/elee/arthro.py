"""
Άρθρο λογιστικής
"""
from . import utils as ul
from .settings import FORMAT_LINE
from . import arthro_line


class Arthro():
    def __init__(self, date, parastatiko, perigrafi):
        self.dat = date
        self.par = parastatiko
        self.per = perigrafi
        self.lines = []

    def add_line(self, lmo, xre, pis):
        self.lines.append(arthro_line.Line(lmo, xre, pis))

    def add_final(self, lmo):
        assert len(self.lines) > 0
        ypol = self.ypoloipo
        if ypol == 0:
            return
        elif ypol > 0:
            self.add_line(lmo, 0, ypol)
        else:
            self.add_line(lmo, ypol * -1, 0)

    def add(self, line):
        """Εδώ πρέπει να σιγουρέψουμε ότι το line είναι instance του
           arthro-line
        """
        self.lines.append(line)

    def similarities(self):
        '''Find similarities between accounts'''
        print(', '.join([lm.lmo for lm in self.lines]))

    @property
    def typos(self):
        tset = set()
        for lin in self.lines:
            tset = tset.union(lin.typos)
        return tset

    @property
    def ee_typos(self):
        if 'ΕΕ ΕΣΟΔΑ' in self.typos:
            return '7'
        elif 'ΕΕ ΕΞΟΔΑ' in self.typos:
            return '26'
        elif '1' in self.typos:
            return '1'
        else:
            return 'ΛΑΘΟΣ'

    @property
    def ee_synt(self):
        if 'ΕΕ ΕΣΟΔΑ' in self.typos:
            return ul.dec(-1)
        elif 'ΕΕ ΕΞΟΔΑ' in self.typos:
            return ul.dec(1)
        elif '1' in self.typos:
            return ul.dec(1)
        else:
            return ul.dec(0)

    def is_typos(self, typos):
        return typos in self.typos

    @property
    def lmoi(self):
        '''List with arthro lmoi'''
        return [line.lmo for line in self.lines]

    @property
    def number_of_lines(self):
        '''Number of lines'''
        return len(self.lines)

    @property
    def val(self):
        assert self.is_complete
        return sum([line.xre for line in self.lines])

    @property
    def is_complete(self):
        rule1 = self.number_of_lines >= 2
        rule2 = self.ypoloipo == 0
        rule3 = sum([line.delta_abs for line in self.lines]) > 0
        return rule1 and rule2 and rule3

    @property
    def ypoloipo(self):
        txre = sum([line.xre for line in self.lines])
        tpis = sum([line.pis for line in self.lines])
        return txre - tpis

    def __repr__(self):
        sst = 'Ημ/νία: %s\nΠαραστατικό: %s\nΠεριγραφή: %s\n'
        ast = sst % (ul.greek_date_from_iso(self.dat), self.par, self.per)
        txr = tpi = ul.dec(0)
        for line in self.lines:
            ast += ' %s\n' % line
            txr += line.xre
            tpi += line.pis
        ast += ' ' + FORMAT_LINE % ('Σύνολο', txr, tpi)
        return ast
