from decimal import Decimal as dec
from collections import namedtuple
from collections import defaultdict
FPA = '54.00'
FPS = [.24, .13, .17]
APC = ('1', '2', '6', '7')
LMO_SPLITTER = '.'


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
    return trah, trad, dper, dlmo, arthro, unparsed_lines


class Trans:
    def __init__(self, dtrh, dtrd, dper, dlmo, dart, unparsed_lines):
        self.dtrh = dtrh  # {trno: (dat par), ...}
        self.dtrd = dtrd  # {aa: (tno lmo xre pis), ...}
        self.dper = dper  # {trno: (per pe2), ...}
        self.dlmo = dlmo  # {lmo: lmoper, ...}
        self.dart = dart  # {trno: [aa_1, aa2, ...], ...}
        self.lerr = unparsed_lines

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
        arthro = self.dart.get(arthro_num, None)
        dfic = {}
        for lno in arthro:
            egr = self.dtrd[lno]
            dfic[egr.lmo] = dfic.get(egr.lmo, dec(0)) + egr.xre - egr.pis
        return dfic

    def arthro_print(self, arthro_num):
        print(self.arthro_dic(arthro_num))

    def check_fpa(self, thold=0.01):
        for arthro_no in self.dart:
            arthro = self.arthro_dic(arthro_no)
            if not is_arthro_for_fpa(arthro):
                continue
            mached = match_accounts(arthro.keys())
            for pair in mached:
                poso = arthro[pair[0]]
                fpa = arthro[pair[1]]
                pfpa = [dec(.24), dec(.13), dec(.17)]
                deltas = [abs(fpa - poso * s) < thold for s in pfpa]
                tfv = [1 if i else 0 for i in deltas]
                if sum(tfv) < 1:
                    print(arthro_no, self.dtrh[arthro_no].dat, arthro)
                    print('')

    def check_fpa2(self, thold=0.02):
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
                    for i, f in enumerate(FPS):
                        isok = abs(arthro[lmo] * dec(f) - arthro[fpa]) < thold
                        if isok:
                            sums[lmo][fpa] = sums[lmo].get(fpa, 0) + 1
                            break
        for lmo in sorted(sums):
            print(lmo, sums[lmo])


def is_arthro_for_fpa(arthro_dic):
    if len(arthro_dic) == 2:
        return False
    kinoymenos = fpa = False
    for lmo in arthro_dic:
        if lmo.startswith(APC):
            kinoymenos = True
        elif lmo.startswith(FPA):
            fpa = True
    return kinoymenos and fpa


def make_combinations(ls1, ls2):
    import itertools
    assert len(ls1) >= len(ls2)

    def split(lst, num):
        return [lst[stt:stt+num] for stt in range(0, len(lst), num)]

    av1 = list([zip(x, ls2) for x in itertools.permutations(ls1, len(ls2))])
    fls = []
    for val in av1:
        for elm in val:
            fls.append(elm)
    return split(fls, len(ls2))


def rank(lmo, fpa):
    clmo = lmo.replace(LMO_SPLITTER, '')
    cfpa = fpa[len(FPA)+1:].replace(LMO_SPLITTER, '')
    score = 0
    for lchar in clmo:
        if lchar in cfpa:
            score += 1
            s = cfpa.index(lchar)
            cfpa = cfpa[:s] + cfpa[s+1:]
    return score


def rank_comb(comb):
    result = 0
    for elm in comb:
        result += rank(elm[0], elm[1])
    return result


def kin_fpa(account_list):
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


def match_accounts(account_list):
    """
    ['24.00.2024', '54.00.2424', '50.00.0000']
    """
    moving_accounts = []
    vat_accounts = []
    for acc in account_list:
        if acc.startswith(APC):
            moving_accounts.append(acc)
        elif acc.startswith(FPA):
            vat_accounts.append(acc)
    # Δεν μπορεί οι λογαριασμοί φπα να είναι περισσότεροι από τους κανονικούς
    assert len(vat_accounts) <= len(moving_accounts)
    # Η απλή περίπτωση
    if len(vat_accounts) == len(moving_accounts) == 1:
        return ((moving_accounts[0], vat_accounts[0]),)
    combs = make_combinations(moving_accounts, vat_accounts)
    result = {}
    for comb in combs:
        result[tuple(comb)] = rank_comb(comb)
    return sorted(result, key=result.get, reverse=True)[0]


if __name__ == '__main__':
    trans = Trans(*parse_imerologio('/home/ted/tmp/fpa/el201809.txt'))
    # trans.isozygio_print(apo='2018-01-01', eos='2018-09-30', not_full=False)
    # trans.kartella_print('60.00')
    # print_vals('el201809.txt')
    # print(match_accounts(['24.00.2024', '54.00.2424',
    #                       '25.00.2024', '54.00.2524',
    #                       '50.00.0000']))
    # print(match_accounts(('25.00.2000', '54.00.2524', '25.00.2024', '50.00.0000')))
    # print(match_accounts(['54.00.29.024', '64.02.06.013',
    #                       '54.00.29.013', '64.02.06.024']))
    # trans.arthro_print(127)
    trans.check_fpa2(0.3)
