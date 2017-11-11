'''Basic module'''
import utils as ul

FORMAT_LINE = '%-15s %12s %12s'
SPLIT_CHAR = '.'
LM1 = ul.read_txt_to_dict('log_sxedio.txt')


class Line():
    def __init__(self, lmo, xre, pis):
        self.lmo = lmo
        self.xre = ul.dec(xre)
        self.pis = ul.dec(pis)

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
        if self.lmo.startswith('38'):
            typ.add('ΜΕΤΡΗΤΑ')
        if self.lmo.startswith('4'):
            typ.add('ΚΕΦΑΛΑΙΟ')
        if self.lmo.startswith('5'):
            typ.add('ΥΠΟΧΡΕΩΣΕΙΣ')
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

    @property
    def y(self):
        return self.xre - self.pis

    @property
    def gy(self):
        return ul.dec2gr(self.y)

    @property
    def gxre(self):
        return ul.dec2gr(self.xre)

    @property
    def gpis(self):
        return ul.dec2gr(self.pis)

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

    def __str__(self):
        return FORMAT_LINE % (self.lmo, self.gxre, self.gpis)


class Arthro():
    def __init__(self, dat, par, per, lines=None):
        self.dat = dat
        self.par = par
        self.per = per
        if lines:
            self.z = lines
        else:
            self.z = []

    def similarities(self):
        '''Find similarities between accounts'''
        print(', '.join([lm.lmo for lm in self.z]))

    @property
    def typos(self):
        tset = set()
        for line in self.z:
            tset = tset.union(line.typos)
        # if {'ΦΠΑ', 'ΑΓΟΡΕΣ'}.issubset(tset):
        #     tset.add('ΑΓΟΡΕΣ ΜΕ ΦΠΑ')
        # if {'ΑΓΟΡΕΣ', 'ΠΡΟΜΗΘΕΥΤΕΣ'}.issubset(tset):
        #     tset.add('ΑΓΟΡΕΣ ΕΠΙ ΠΙΣΤΩΣΕΙ')
        return tset

    @property
    def ee_typos(self):
        if 'ΕΕ ΕΣΟΔΑ' in self.typos:
            return 'ΕΣ'
        elif 'ΕΕ ΕΞΟΔΑ' in self.typos:
            return 'ΕΞ'
        elif '1' in self.typos:
            return 'ΠΑ'
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
        return [line.lmo for line in self.z]

    @property
    def zlines(self):
        '''Number of lines'''
        return len(self.z)

    def add(self, line):
        self.z.append(line)

    @property
    def val(self):
        return sum([line.xre for line in self.z])

    @property
    def is_complete(self):
        total = sum([line.y for line in self.z])
        abstotal = sum([abs(line.y) for line in self.z])
        return total == 0 and abstotal > 0

    def __str__(self):
        ast = '%s %s %s\n' % (self.dat, self.par, self.per)
        txr = tpi = ul.dec(0)
        for line in self.z:
            ast += ' %s\n' % line
            txr += line.xre
            tpi += line.pis
        ast += ' ' + FORMAT_LINE % ('Σύνολο', txr, tpi)
        return ast


class Book():
    def __init__(self, lmoi=None, arthra=None):
        # self.lmoi = lmoi
        self.lmoi = {**lmoi, **LM1}
        self.arthra = arthra

    def add_arthro(self, arthro):
        self.arthra.append(arthro)
        for lmo in arthro.lmoi:
            if lmo not in self.lmoi:
                self.lmoi[lmo] = {}

    @property
    def typoi(self):
        typoi = set()
        for arthro in self.arthra:
            typoi = typoi.union(arthro.typos)
        return typoi

    def isozygio(self, apo, eos, typos=None):
        isoz = {}
        for arthro in self.arthra:
            if not apo <= arthro.dat <= eos:
                continue
            if typos and not arthro.is_typos(typos):
                continue
            for line in arthro.z:
                for lmo in line.hierarchy:
                    isoz[lmo] = isoz.get(lmo, ul.dec(0)) + line.y
        return isoz

    def isozygio_print(self, apo, eos, typos=None):
        isoz = self.isozygio(apo, eos, typos)
        tst = '%-20s %-50s %12s'
        print('Ισοζύγιο από %s έως %s %s' % (apo, eos, typos or 'ΟΛΑ'))
        for lmo in sorted(isoz):
            print(tst % (lmo, self.lmoi.get(lmo, lmo), isoz[lmo]))

    def kartella(self, lmos, apo, eos):
        fdata = []
        total = ul.dec(0)
        before = ul.dec(0)
        after = ul.dec(0)
        for arthro in self.arthra:
            for line in arthro.z:
                if lmos in line.hierarchy:
                    if arthro.dat < apo:
                        before += line.y
                    elif arthro.dat > eos:
                        after += line.y
                    else:
                        total += line.y
                        fdata.append((arthro.dat, arthro.par, arthro.per,
                                      line.xre, line.pis, total))
        return fdata, before, after

    def kartella_print(self, lmos, apo, eos):
        data, before, after = self.kartella(lmos, apo, eos)
        ast = 'Καρτέλλα Λογαριασμού %s %s (Άπό: %s Έως: %s)'
        print(ast % (lmos, self.lmoi[lmos], apo, eos))
        print('%-139s %12s' % ('Υπόλοιπο από μεταφορά', before))
        for dat in data:
            # print(len(dat[2]))
            print('%-10s %-26s %-75s %12s %12s %12s' % dat)

    def fpa(self, apo, eos):
        pass

    def arthra_print(self, typos=None):
        headt = "%-6s %-10s %s %s %s"
        lit = "  %-12s %-40s %12s %12s"
        i = 0
        for art in self.arthra:
            if typos and typos not in art.typos:
                continue
            i += 1
            print(headt % (i, art.dat, art.par, art.per, art.typos))
            for lin in art.z:
                print(lit % (lin.lmo, self.lmoi.get(lin.lmo, lin.lmo),
                             lin.xre, lin.pis))
            print('')

    def eebook(self):
        i = 0
        lins = []
        for art in self.arthra:
            if 'ΕΕ' not in art.typos:
                continue
            i += 1
            poso = ul.dec(0)
            fpa = ul.dec(0)
            for line in art.z:
                if '54.00' in line.typos:
                    fpa += ul.dec(line.y * art.ee_synt)
                elif '1' in line.typos:
                    poso += ul.dec(line.xre * art.ee_synt)
                elif '2' in line.typos:
                    poso += ul.dec(line.y * art.ee_synt)
                elif '6' in line.typos:
                    poso += ul.dec(line.y * art.ee_synt)
                elif '7' in line.typos:
                    poso += ul.dec(line.y * art.ee_synt)
                else:
                    pass
            lins.append((i, art.dat, art.ee_typos, art.par, art.per,
                         poso, fpa, art.val, art.val - poso - fpa))
        return lins

    def eebook_print(self):
        eedata = self.eebook()
        sta = '%-5s %-10s %2s %-22s %-75s %12s %12s %12s %10s'
        for line in eedata:
            print(sta % line)

    def eebook_totals(self, apo, eos):
        eedata = self.eebook()
        eposo = efpa = xposo = xfpa = ul.dec(0)
        for line in eedata:
            if not (apo <= line[1] <= eos):
                continue
            if line[2] == 'ΕΣ':
                eposo += line[5]
                efpa += line[6]
            elif line[2] in ('ΕΞ', 'ΠΑ'):
                xposo += line[5]
                xfpa += line[6]
            else:
                print('Error')
        print('Σύνολα για περίοδο από %s έως %s' % (apo, eos))
        print('Έσοδα  : %15s ΦΠΑ: %15s' % (eposo, efpa))
        print('Έξοδα  : %15s ΦΠΑ: %15s' % (xposo, xfpa))
        print('Διαφορά: %15s      %15s' % (eposo - xposo, efpa - xfpa))

    def __str__(self):
        stf = ''
        for arthro in self.arthra:
            stf += '%s\n' % arthro.__str__()
        return stf
