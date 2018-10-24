from decimal import Decimal as dec
from collections import namedtuple
from collections import defaultdict
FPA = '54.00'
FPS = [.24, .13, .17]  # Συντελεστές ΦΠΑ
APC = ('1', '2', '6', '7')  # Ομάδες αποτελεσμάτων
LMO_SPLITTER = '.'  # Διαχωριστικό λογαριασμών


def iso_dat(greek_date):
    """Μετατρέπει μια iso Ημερομηνία σε Ελληνική"""
    dd, mm, yyyy = greek_date.split('/')
    return '%s-%s-%s' % (yyyy, mm, dd)


def lmo_hierarchy(lmo):
    """Δημιουργία λίστας με την ιεραρχία του λογαριασμου
       πχ ο λογαριασμός 20.00.00 δίνει ['2', '20', '20.00', '20.00.00']
    """
    als = lmo.split(LMO_SPLITTER)
    ranks = ['.'.join(als[:i]) for i in range(len(als))]
    ranks[0] = lmo[0]  # Προσθήκη της ομάδας στους λογαριασμούς
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
    Dpe = namedtuple('Dpe', 'per pe2')
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
                dper[tno] = Dpe(per, pe2)
            else:
                unparsed_lines[i] = lin
    # print(arthro)
    # print(dper)
    # print(dlmo)
    # print(unparsed_lines)
    return {'tr_header': trah, 'tr_lines': trad, 'tr_per': dper,
            'lmoi': dlmo, 'arthra': arthro, 'errors': unparsed_lines}


def kin_fpa(account_list):
    """Από μια λίστα λογαριασμών επιστρέφει διαχωρισμένους
       χωριστά τους αποτελεσματικούς και τους λ/μούς ΦΠΑ
    """
    apoac = []
    fpaac = []
    kinoymenos = fpa = False
    for acc in account_list:
        if acc.startswith(APC):
            apoac.append(acc)
            kinoymenos = True
        elif acc.startswith(FPA):
            fpaac.append(acc)
            fpa = True
    assert kinoymenos and fpa
    return {'apc': apoac, 'fpa': fpaac}


def is_arthro_for_fpa(arthro_dic):
    """Ελέγχει αν το άρθρο είναι κίνηση με ΦΠΑ"""
    # Αν το άρθρο έχει 2 γραμμές δεν λαμβάνεται υπ'οψιν
    if len(arthro_dic) == 2:
        return False
    kinoymenos = fpa = False
    for lmo in arthro_dic:
        # Ο λογαριασμός είναι αποτελεσματικός
        if lmo.startswith(APC):
            kinoymenos = True
        # Είναι λογαριασμός ΦΠΑ
        elif lmo.startswith(FPA):
            fpa = True
    return kinoymenos and fpa


class Trans:
    def __init__(self, parsed):
        self.dtrh = parsed['tr_header']  # {trno: (dat par), ...}
        self.dtrd = parsed['tr_lines']  # {aa: (tno lmo xre pis), ...}
        self.dper = parsed['tr_per']  # {trno: (per pe2), ...}
        self.dlmo = parsed['lmoi']  # {lmo: lmoper, ...}
        self.dart = parsed['arthra']  # {trno: [aa_1, aa2, ...], ...}
        self.lerr = parsed['errors']  # Λάθη (γραμμές που δεν πέρασαν)

    def __str__(self):
        stt = 'Arthra   : %5s\nLines    : %5s\nAccounts : %5s\nErrors   : %5s'
        return stt % (len(self.dart), len(self.dtrd),
                      len(self.dlmo), len(self.lerr))

    def info(self):
        print(self)

    def isozygio(self, apo=None, eos=None, not_full=False):
        dis = defaultdict(lambda: [dec(0), dec(0), dec(0)])
        dfi = defaultdict(lambda: [dec(0), dec(0), dec(0)])
        for lin in self.dtrd.values():
            if apo:
                if self.dtrh[lin.tno].dat < apo:
                    continue
            if eos:
                if self.dtrh[lin.tno].dat > eos:
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
        for lin in self.dtrd.values():
            if lin.lmo.startswith(lmos):
                rsum += lin.xre - lin.pis
                lva = Kar(lin.tno, self.dtrh[lin.tno].dat,
                          self.dtrh[lin.tno].par, self.dper[lin.tno].per,
                          lin.xre, lin.pis, rsum)
                val.append(lva)
        return val

    def kartella_print(self, lmos):
        kar = self.kartella(lmos)
        stt = '%5s %10s %-20s %-70s %12s %12s %12s'
        # tno dat par lmo xre pis
        for lin in kar:
            print(stt % (lin.tno, lin.dat, lin.par, lin.per, lin.xre,
                         lin.pis, lin.sum))

    def arthro_dic(self, arthro_num):
        """Επιστρέφει: {'20.00': 100, '54.00': 24, '50.00': -124}"""
        arthro = self.dart.get(arthro_num, None)
        dfic = {}
        for lno in arthro:
            egr = self.dtrd[lno]
            # Εάν υπάρχουν παραπάνω από μία γραμμές με τον ίδιο κωδικό
            # λογιστικής αθροίζονται σε μία
            dfic[egr.lmo] = dfic.get(egr.lmo, dec(0)) + egr.xre - egr.pis
        return dfic

    def arthro_print(self, arthro_num):
        print(self.arthro_dic(arthro_num))

    def fpa_find_pairs(self, thold=0.02):
        """Βρίσκουμε ζευγάρια λογαριασμών της μορφής:
            {'62.03.02.024': ('54.00.29.024', 0.24), ...}
           Για να είναι εντάξει χρειάζεται κάθε λογαριασμός να έχει ένα
           και μοναδικό αντίστοιχο λογαριασμό ΦΠΑ η τουλάχιστον ίδιο
           συντελεστή ΦΠΑ.
        """
        sums = {}
        for arthro_no in self.dart:
            arthro = self.arthro_dic(arthro_no)
            if not is_arthro_for_fpa(arthro):
                continue
            ar_acc = kin_fpa(arthro.keys())
            for lmo in ar_acc['apc']:
                sums[lmo] = sums.get(lmo, {})
                for fpa in ar_acc['fpa']:
                    # FPS = [.24, .13, .17]
                    # Δοκιμάζουμε με τους ισχύοντες συντελεστές ΦΠΑ
                    for f in FPS:
                        isok = abs(arthro[lmo] * dec(f) - arthro[fpa]) < thold
                        if isok:
                            # Δημιουργούμε tuple ('54.00.29.024', dec(.24))
                            fpav = (fpa, round(dec(f), 2))
                            sums[lmo][fpav] = sums[lmo].get(fpav, 0) + 1
                            break
        mat = {}
        for lmo in sorted(sums):
            Mvl = namedtuple('Mvl', 'fpaa synt')
            mached = sorted(sums[lmo], key=sums[lmo].get, reverse=True)
            fpaa = ''
            synt = 0
            if mached:
                mach = mached[0]
                fpaa, synt = mach
            mat[lmo] = Mvl(fpaa, synt)
            # print(lmo, sums[lmo])
        print(mat)
        return mat

    def check_fpa(self, thres=0.02):
        # Βρές ζευγάρια λογαριασμών
        pairs = self.fpa_find_pairs()
        err = ''
        stt = '%s %s %s %s\n\n'
        for ar_no in self.dart:
            arthro = self.arthro_dic(ar_no)
            if not is_arthro_for_fpa(arthro):
                continue
            ar_acc = kin_fpa(arthro.keys())
            for lmo in ar_acc['apc']:
                lmo_fpa = pairs[lmo].fpaa
                if not lmo_fpa:
                    continue
                syn_fpa = pairs[lmo].synt
                assert lmo_fpa in ar_acc['fpa']
                delta = arthro[lmo] * syn_fpa - arthro[lmo_fpa]
                if not (abs(delta) <= thres):
                    err += stt % (ar_no, self.dtrh[ar_no], arthro, delta)
        if err == '':
            err = 'Everything is ok. No fpa problems found :-)'
        return err


if __name__ == '__main__':
    trans = Trans(parse_imerologio('/home/ted/tmp/fpa/el201809.txt'))
    # trans.isozygio_print(apo='2018-01-01', eos='2018-09-30', not_full=False)
    # trans.kartella_print('60.00')
    # trans.arthro_print(127)
    print(trans.check_fpa())
