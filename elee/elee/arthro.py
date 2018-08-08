"""
Άρθρο λογιστικής
"""
from . import utils as ul
from . import settings as stt
from . import arthro_line


class Arthro():
    def __init__(self, date, parastatiko, perigrafi, arthro_number=0, pe2=''):
        self.num = arthro_number
        self.dat = date
        self.par = parastatiko
        self.per = perigrafi
        self.pe2 = pe2
        self.lines = []

    def check_fpa1(self):
        assert self.is_complete
        if self.number_of_lines == 2:
            return -1  # Δεν μπορεί ένα άρθρο με 2 γραμμές να έχει ΦΠΑ
        fpa = {}
        l4fpa = {}
        for lin in self.lines:
            if lin.lmo.startswith(stt.FPA_LMO):
                fpa[lin.lmo] = fpa.get(lin.lmo, 0) + lin.delta
            elif lin.lmo[0] in stt.FPA_OMADES:
                l4fpa[lin.lmo] = l4fpa.get(lin.lmo, 0) + lin.delta
        lfpa = ul.calc_synt_dict(l4fpa, stt.FPA_SYNTELESTES)
        delta = {}
        for lmofpa, valfpa in fpa.items():
            for lmoom, valom in lfpa.items():
                dmin = {}
                for pfpa, vfpa in valom.items():
                    dif = abs(valfpa - vfpa)
                    dmin[pfpa] = dif
                pkey = min(dmin, key=dmin.get)
                pval = dmin[pkey]
                key = '%s|%s|%s' % (lmofpa, lmoom, pkey)
                if pval <= stt.THRESHOLD:
                    delta[key] = pval
        return fpa, l4fpa, lfpa, delta

    @property
    def is_ee(self):
        assert self.is_complete
        for lin in self.lines:
            # print(self.num, lin.lmo[0])
            if lin.lmo[0] in stt.EE_OMADES:
                return True
        return False

    @property
    def esej(self):
        if not self.is_ee:
            return None
        lval = []
        val = []
        lfpa = []
        fpa = []
        for lin in self.lines:
            if lin.lmo.startswith(stt.FPA_LMO):
                lfpa.append(lin.lmo)
                fpa.append(lin.delta)
            elif lin.lmo[0] in stt.EE_OMADES:
                lval.append(lin.lmo)
                val.append(lin.delta)
        lst = [self.num, self.dat, self.par, self.per, self.pe2,
               sum(val), sum(fpa), sum(val) + sum(fpa)]
        return lst

    def check_fpa(self):
        assert self.is_complete
        if self.number_of_lines == 2:
            return -1  # Δεν μπορεί ένα άρθρο με 2 γραμμές να έχει ΦΠΑ
        lval = []
        val = []
        lfpa = []
        fpa = []
        for lin in self.lines:
            if lin.lmo.startswith(stt.FPA_LMO):
                lfpa.append(lin.lmo)
                fpa.append(lin.delta)
            elif lin.lmo[0] in stt.FPA_OMADES:
                lval.append(lin.lmo)
                val.append(lin.delta)
        val_len, val_fpa = len(lval), len(lfpa)
        if val_len == 0 or val_fpa == 0:
            return True
        assert val_len >= val_fpa  # Οι γραμμές ΦΠΑ πάντα λιγότερες/ίσες
        for i, _ in enumerate(lfpa):
            if val[i] < 1 and fpa[i] < 0.24:
                continue
            synt = ul.closer(fpa[i] / val[i] * 100, stt.FPA_SYNTELESTES)
            diff = abs(ul.dec(val[i] * ul.dec(synt)/ ul.dec(100)) - fpa[i])
            if diff > stt.THRESHOLD:
                print('Error in %s' % self.num)
                print('Diff %s > %s (synt=%s%%)' % (diff, stt.THRESHOLD, synt))
                return False
        return True

    def add_line(self, lmo, xre, pis, line_number=None):
        if not line_number:
            line_number = len(self.lines) + 1
        self.lines.append(arthro_line.Line(lmo, xre, pis, line_number))

    def lins(self, line_number):
        if line_number < len(self.lines):
            return self.lines[line_number]
        return None

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
    def htyp(self):
        """
        Τύπος άρθρου. Πχ 3 χρέωση, 7 πίστωση, 54.00 πίστωση πωλήσεις
        {'3': 1, '7': 2, '54.00': 2} πωλήσεις
        {'3': -1, '7': -2, '54.00': -2} Αντίστροφο
        {'30.00': 1, '70.01': 2, '54.00': 2}
        '3:1|54.00:2|7:2'
        """
        set_type = set()
        for line in self.lines:
            set_type = set_type.union(line.htyp)
        return set_type

    def category(self, dict_of_categories):
        # print(self)
        categories = 'ERROR'
        for name, cat_set in dict_of_categories.items():
            if cat_set < self.htyp:
                categories = name
                break
        return categories

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
        sst = '\nNo: %s\nΗμ/νία: %s\nΠαραστατικό: %s\nΠεριγραφή: %s\nΠ2: %s\n'
        grdate = ul.greek_date_from_iso(self.dat)
        ast = sst % (self.num, grdate, self.par, self.per, self.pe2)
        txr = tpi = ul.dec(0)
        for line in self.lines:
            ast += ' %s\n' % line
            txr += line.xre
            tpi += line.pis
        ast += ' ' + stt.FORMAT_LINE % ('', 'Σύνολο', txr, tpi)
        return ast
