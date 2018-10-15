from decimal import Decimal as dec
from collections import namedtuple
from collections import defaultdict


def iso_dat(greek_date):
    dd, mm, yyyy = greek_date.split('/')
    return '%s-%s-%s' % (yyyy, mm, dd)


def lmo_hierarchy(lmo, split_char='.'):
    als = lmo.split(split_char)
    ranks = ['.'.join(als[:i]) for i in range(len(als))]
    ranks[0] = lmo[0]
    return ranks


def parse_imerologio(fil, enc='WINDOWS-1253'):
    # Create list with startwith
    exc = (' ' * 150 + 'Σελίδα',
           ' ' * 33 + 'ΓΕΝΙΚΟ ΗΜΕΡΟΛΟΓΙΟ',
           '  Ημ/νία      Α/Α ΚΒΣ Στοιχεία Αρθρου',
           '  Ημ/νία     Α/Α ΚΒΣ  Στοιχεία Αρθρου',
           '                      Σχετ. Παραστατ.',
           '  -----------------------------------',
           ' ' * 38 + 'Από μεταφορά',
           ' ' * 123 + '-------------- --------------',
           ' ' * 70 + 'Σύνολα Σελίδας',
           ' ' * 70 + 'Σε Μεταφορά',
           ' ' * 70 + 'Σύνολα Περιόδου',
           ' ' * 152
           )
    dat = par = lmo = lmp = xre = pis = pe2 = per = ''
    tno = lno = 0
    sdat = slice(2, 12)
    spar = slice(22, 48)
    slmo = slice(48, 60)
    slmp = slice(77, 122)
    sxre = slice(124, 137)
    spis = slice(139, 152)
    spe2 = slice(22, 48)
    # sper = slice(48, 152)
    dper = {}
    dlmo = {}
    trah = {}
    trad = {}
    arthro = {}
    unparsed_lines = {}
    # fts = '%s %20s %12s %12s %12s %5s %5s'
    Trd = namedtuple('Trd', 'tno lmo xre pis')
    Trh = namedtuple('Trh', 'dat par')
    with open(fil, encoding=enc) as ofil:
        for i, lin in enumerate(ofil):
            llin = len(lin)  # Το υπολογίζω εδώ μία φορά
            if llin < 48:  # Δεν έχουν νόημα γραμμές μικρότερες του 48
                continue
            elif lin.startswith(exc):
                continue
            elif lin[50] == '.' and lin[53] == '.' and lin[134] == ',':
                if lin[4] == '/' and lin[7] == '/':
                    tno += 1
                    dat = iso_dat(lin[sdat])
                    par = lin[spar].strip()
                    trah[tno] = Trh(dat, par)
                lno += 1
                lmo = lin[slmo].strip()
                lmp = lin[slmp].strip()
                xre = dec(lin[sxre].strip().replace('.', '').replace(',', '.'))
                pis = dec(lin[spis].strip().replace('.', '').replace(',', '.'))
                if lmo in dlmo:
                    if dlmo[lmo] != lmp:
                        print('Διαφορά στο όνομα %s -> %s' % (dlmo[lmo], lmp))
                else:
                    dlmo[lmo] = lmp
                trad[lno] = Trd(tno, lmo, xre, pis)
                arthro[tno] = arthro.get(tno, [])
                arthro[tno].append(lno)
                # print(fts % (dat, par, lmo, xre, pis, tno, trlinno))
            elif llin < 132:  # Πρόκειται για γραμμή περιγραφής
                pe2 = lin[spe2].strip()
                per = lin[48:-1].strip()
                dper[tno] = {'per': per, 'pe2': pe2}
            else:
                unparsed_lines[i] = lin
    # print(arthro)
    # print(dper)
    # print(dlmo)
    # print(unparsed_lines)
    return trah, trad, dper, dlmo, arthro, unparsed_lines


class Trans:
    def __init__(self, trah, trad, dper, dlmo, arthra, unparsed_lines):
        self.trah = trah  # Dictionary of named tuple trh
        self.trad = trad
        self.dper = dper
        self.dlmo = dlmo
        self.arth = arthra
        self.err = unparsed_lines

    def __str__(self):
        stt = 'Arthra   : %5s\nLines    : %5s\nAccounts : %5s\nErrors   : %5s'
        return stt % (len(self.arth), len(self.trad),
                      len(self.dlmo), len(self.err))

    def info(self):
        print(self)

    def isozygio(self, apo=None, eos=None, not_full=False):
        dis = defaultdict(lambda: [dec(0), dec(0), dec(0)])
        dfi = defaultdict(lambda: [dec(0), dec(0), dec(0)])
        for lin in self.trad.values():
            if apo:
                if self.trah[lin.tno].dat < apo:
                    continue
            if eos:
                if self.trah[lin.tno].dat > eos:
                    continue
            dis[lin.lmo][0] += lin.xre
            dis[lin.lmo][1] += lin.pis
            dis[lin.lmo][2] += lin.xre - lin.pis
        if not_full:
            return dis
        # Για λόγους ταχύτητας κάνουμε εδώ τους ανωτεροβάθμιους
        for lmo, vals in dis.items():
            for plmo in lmo_hierarchy(lmo):
                dfi[plmo][0] += vals[0]
                dfi[plmo][1] += vals[1]
                dfi[plmo][2] += vals[2]
            dfi[lmo] = vals
        return dfi

    def isozygio_print(self, apo=None, eos=None, not_full=False):
        dis = self.isozygio(apo, eos, not_full)
        stt = '%-12s %-50s %12s %12s %12s'
        for lmo, val in sorted(dis.items()):
            print(stt % (lmo, self.dlmo.get(lmo, ''), val[0], val[1], val[2]))

    def kartella(self, lmos, apo=None, eos=None):
        Kar = namedtuple('Kar', 'tno dat par per xre pis sum')
        val = []
        rsum = dec(0)
        for lin in self.trad.values():
            if lin.lmo.startswith(lmos):
                rsum += lin.xre - lin.pis
                lva = Kar(lin.tno, self.trah[lin.tno].dat,
                          self.trah[lin.tno].par, self.dper[lin.tno]['per'],
                          lin.xre, lin.pis, rsum)
                val.append(lva)
        return val

    def kartella_print(self, lmos):
        kar = self.kartella(lmos)
        stt = '%5s %10s %-20s %-50s %12s %12s %12s'
        # tno dat par lmo xre pis
        for lin in kar:
            print(stt % (lin.tno, lin.dat, lin.par, lin.per, lin.xre,
                         lin.pis, lin.sum))

    def arthro(self, arthro_num):
        arthro = self.arth.get(arthro_num, None)
        return [self.trad[lin] for lin in arthro]

    def arthro_print(self, arthro_num):
        pass


if __name__ == '__main__':
    trans = Trans(*parse_imerologio('/home/ted/tmp/fpa/el201809.txt'))
    trans.isozygio_print(apo='2018-07-01', eos='2018-09-30', not_full=False)
    # print_vals('el201809.txt')
