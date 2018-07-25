"""
Αναλυτική γραμμή άρθρου λογιστικής
"""
from . import utils as ul
from .settings import SPLIT_CHAR
from .settings import FORMAT_LINE


class Line():
    def __init__(self, lmo, xreosi, pistosi, line_number=0):
        assert (xreosi == 0) or (pistosi == 0)
        assert xreosi != pistosi
        self.num = line_number
        self.lmo = lmo
        self.xre = ul.dec(xreosi)
        self.pis = ul.dec(pistosi)

    def lmop(self, lmodic):
        return lmodic.get(self.lmo, self.lmo)

    @property
    def typos(self):
        typ = set()
        if self.lmo.startswith('1'):
            typ.add('ΠΑΓΙΑ')
            typ.add('ΕΕ')
            typ.add('1')
        if self.lmo.startswith('2'):
            typ.add('ΑΠΟΘΕΜΑΤΑ')
            typ.add('ΕΕ')
            typ.add('ΕΕ ΕΞΟΔΑ')
            typ.add('2')
        if self.lmo.startswith('20'):
            typ.add('ΕΜΠΟΡΕΥΜΑΤΑ')
        if self.lmo.startswith('20.00'):
            typ.add('ΑΠΟΓΡΑΦΗ ΕΜΠΟΡΕΥΜΑΤΩΝ')
        if self.lmo.startswith('20.01'):
            typ.add('ΑΓΟΡΕΣ ΕΜΠΟΡΕΥΜΑΤΩΝ')
            typ.add('ΑΓΟΡΕΣ')
        if self.lmo.startswith('24.01'):
            typ.add("ΑΓΟΡΕΣ Α' ΚΑΙ Β' ΥΛΩΝ")
            typ.add('ΑΓΟΡΕΣ')
        if self.lmo.startswith('3'):
            typ.add('ΑΠΑΙΤΗΣΕΙΣ')
            typ.add('3-5')
        if self.lmo.startswith('38'):
            typ.add('ΜΕΤΡΗΤΑ')
        if self.lmo.startswith('4'):
            typ.add('ΚΕΦΑΛΑΙΟ')
        if self.lmo.startswith('5'):
            typ.add('ΥΠΟΧΡΕΩΣΕΙΣ')
            typ.add('3-5')
        if self.lmo.startswith('50'):
            typ.add('ΠΡΟΜΗΘΕΥΤΕΣ')
        if self.lmo.startswith('54.00'):
            typ.add('ΦΠΑ')
            typ.add('54.00')
        if self.lmo.startswith('6'):
            typ.add('ΕΞΟΔΑ')
            typ.add('ΕΕ')
            typ.add('ΕΕ ΕΞΟΔΑ')
            typ.add('6')
        if self.lmo.startswith('7'):
            typ.add('ΕΣΟΔΑ')
            typ.add('ΠΩΛΗΣΕΙΣ')
            typ.add('ΕΕ')
            typ.add('ΕΕ ΕΣΟΔΑ')
            typ.add('7')
        if self.lmo.startswith('70'):
            typ.add('ΠΩΛΗΣΕΙΣ ΕΜΠΟΡΕΥΜΑΤΩΝ')
        if self.lmo.startswith('71'):
            typ.add('ΠΩΛΗΣΕΙΣ ΠΡΟΪΟΝΤΩΝ')
        if self.lmo.startswith('8'):
            typ.add('ΑΝΟΡΓΑΝΑ')
        return typ

    def is_typos(self, typos):
        return typos in self.typos

    def has_tag(self, tag):
        return tag in self.typos

    @property
    def is_xreostiko(self):
        return self.xre > 0

    @property
    def is_xreostiko_negative(self):
        return self.xre < 0

    @property
    def is_pistotiko(self):
        return self.pis > 0

    @property
    def is_pistotiko_negative(self):
        return self.pis < 0

    @property
    def delta(self):
        return self.xre - self.pis

    @property
    def delta_abs(self):
        return abs(self.xre - self.pis)

    @property
    def gdelta(self):
        return ul.dec2gr(self.delta)

    @property
    def gxre(self):
        return ul.dec2gr(self.xre, True)

    @property
    def gpis(self):
        return ul.dec2gr(self.pis, True)

    @property
    def line_type(self):
        if self.is_xreostiko:
            return 1
        elif self.is_xreostiko_negative:
            return -1
        elif self.is_pistotiko:
            return 2
        elif self.is_pistotiko_negative:
            return -2
        return 0

    @property
    def hierarchy(self):
        assert len(self.lmo) > 1
        listlmo = self.lmo.split(SPLIT_CHAR)
        listfinal = ['t']
        if self.lmo[0] in '267':
            listfinal.append('t267')
        elif self.lmo[0] in '35':
            listfinal.append('t35')
        listfinal.append(self.lmo[0])
        tmp = ''
        for el in listlmo:
            if tmp == '':
                tmp = el
            else:
                tmp = SPLIT_CHAR.join([tmp, el])
            listfinal.append(tmp)
        return listfinal

    @property
    def htyp(self):
        vset = set()
        ltyp = self.line_type
        for hier in self.hierarchy:
            vset.add('%s:%s' % (hier, ltyp))
        return vset

    def __repr__(self):
        return FORMAT_LINE % (self.num, self.lmo, self.gxre, self.gpis)
