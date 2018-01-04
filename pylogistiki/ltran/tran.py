"""
Προσομίωση οικονομικών διαδικασιών.
Έννοιες όπως είδος , τιμολόγιο, εγγραφή, έξοδα, αγορές, κλπ
Ενδεχομενως με βάση τη λογιστική
Ας πούμε
1. Πάγια
2. Αποθέματα
3. Απαιτήσεις
4. Κεφάλαιο
5. Υποχρρεώσεις
6. Έξοδα
7. Έσοδα
8. Ανόργανα
"""
from utils import dec
import json
import gzip
ACCOUNT_TYPES = {'1': ['Πάγια', 'Ενεργητικό'],
                 '2': ['Αποθέματα', 'Ενεργητικό'],
                 '3': ['Απαιτήσεις', 'Ενεργητικό'],
                 '38': ['Ταμιακά'],
                 '4': ['Κεφάλαιο', 'Παθητικό'],
                 '5': ['Υποχρεώσεις', 'Παθητικό'],
                 '54.00': ['ΦΠΑ'],
                 '6': ['Εξοδα'],
                 '7': ['Εσοδα'],
                 '8': ['Ανόργανα'],
                 '80.00': ['Αποτελέσματα', 'Παθητικό']
                 }
ACCOUNT_SPLITTER = '.'
DEBIT, CREDIT = 1, 2
ANOIGMA, GENIKO, KLEISIMO = 1, 2, 3  # Ημερολόγια εγγραφών
APOTELESMATA = '80.00.00'  # Λογαριασμός αποτελεσμάτων
FPA = '54.00'  # Βασικός λογαριασμός ΦΠΑ
FPAF = '54.00.99'  # Λογαριασμός κλεισίματος ΦΠΑ
APOTH = '2'  # Αποθέματα
ESODA = '7'  # Έσοδα
EJODA = '6'  # έξοδα


def levels(account):
    arlev = account.split(ACCOUNT_SPLITTER)  # ['38', '00', '00']
    rlist = [account[0]]  # Βάζουμε την ομάδα
    for i, _ in enumerate(arlev):
        rlist.append('.'.join(arlev[:i + 1]))
    return rlist[:-1]


class TransException(Exception):
    pass


class Account():
    """Λογαριασμός"""

    def __init__(self, cod, name=None):
        assert len(cod) > 0
        self._cod = cod  # Κωδικός λογαριασμού
        # Το όνομα του λογαριασμού δεν είναι απαραίτητο κατά τη δημιουργία
        # Μπορεί να αναζητηθεί από αρχείο
        self._nam = name  # Ονομασία λογαριασμού

    @property
    def code(self):
        return self._cod

    @property
    def name(self):
        return self._nam if self._nam else '??? %s ???' % self._cod

    @property
    def tags(self):
        rlist = []
        for atyp in ACCOUNT_TYPES:
            if self._cod.startswith(atyp):
                rlist += ACCOUNT_TYPES[atyp]
        return rlist

    @property
    def levels(self):
        arlev = self._cod.split(ACCOUNT_SPLITTER)  # ['38', '00', '00']
        rlist = [self._cod[0]]  # Βάζουμε την ομάδα
        for i, _ in enumerate(arlev):
            rlist.append('.'.join(arlev[:i + 1]))
        return rlist

    @property
    def levels_tags(self):
        return self.levels + self.tags

    def __repr__(self):
        # return '%-15s %s (%s)' % (self._cod, self.name, self.tags)
        return '%-15s %s' % (self._cod, self.name)


class TransLine():
    """Λογιστική εγγραφή"""

    def __init__(self, num, pel, typ, poso, acode, aper=None, parent=None):
        assert typ in (CREDIT, DEBIT)
        self._no = num  # Αριθμός γραμμής
        self._acc = Account(acode, aper)  # Λογαριασμός
        self._pel = pel  # Περιγραφή γραμμής
        self._typ = typ  # 1 για χρέωση 2 για πίστωση
        self._val = dec(poso)  # Ποσό
        self._parent = parent

    @property
    def journal(self):
        return self._parent.journal if self._parent else '??? journal ???'

    @property
    def date(self):
        return self._parent.date if self._parent else '??? date ???'

    @property
    def par(self):
        return self._parent.par if self._parent else '??? par ???'

    @property
    def per(self):
        return self._parent.per if self._parent else '??? per ???'

    @property
    def typ(self):
        return self._typ

    @property
    def val(self):
        return self._val

    @property
    def pel(self):
        return self._pel

    @property
    def no(self):
        return self._parent.no if self._parent else '??? no ???'

    @property
    def xre(self):
        return self._val if self._typ == DEBIT else dec(0)

    @property
    def pis(self):
        return self._val if self._typ == CREDIT else dec(0)

    @property
    def ypo(self):
        return self.xre - self.pis

    @property
    def code(self):
        return self._acc.code

    @property
    def codep(self):
        return self._acc.name

    @property
    def levels(self):
        return self._acc.levels

    @property
    def levels_tags(self):
        return self._acc.levels_tags

    def __repr__(self):
        ast = '%4s %-90s %-20s %12s %12s'
        return ast % (self._no, self._acc, self._pel, self.xre, self.pis)


class Tran():
    """Λογιστικό άρθρο"""

    def __init__(self, date, par, per, journal=2, dic=None):
        """Εγγραφή λογιστικής"""
        if dic:
            self._journal = dic['journal']
            self._dat = dic['dat']
            self._par = dic['par']
            self._per = dic['per']
            self._lns = []
            self._nol = 0
            self._total_debit = dec(0)
            self._total_credit = dec(0)
            self._bal = dec(0)
            for elm in dic['lns']:
                self.line(elm['pel'],
                          elm['typ'],
                          elm['poso'],
                          elm['cod'],
                          elm['codp'])
        else:
            self._journal = journal
            self._no = 0
            self._dat = date  # Ημερομηνία εγγραφής
            self._par = par  # Παραστατικό
            self._per = per  # Περιγραφή
            self._lns = []  # Λίστα με αναλυτικές γραμμές
            self._nol = 0  # Αριθμός γραμμών
            self._total_debit = dec(0)  # συνολική χρέωση
            self._total_credit = dec(0)  # συνολική πίστωση
            self._bal = dec(0)  # Υπόλοιπο (χρεώσεις - πιστώσεις)

    @property
    def to_dict(self):
        """Εξαγωγή δεδομένων σε dictionary"""
        dic = {'journal': self._journal,
               'dat': self._dat,
               'par': self._par,
               'per': self._per,
               'lns': []}
        for lin in self._lns:
            dic['lns'].append({'pel': lin.pel,
                               'typ': lin.typ,
                               'poso': float(lin.val),
                               'cod': lin.code,
                               'codp': lin.codep})
        return dic

    def line(self, per, typ, poso, accode, acper=None):
        self._lns.append(TransLine(self._nol + 1, per, typ, poso,
                                   accode, acper, self))
        self._nol += 1
        if typ == DEBIT:
            self._bal += dec(poso)
            self._total_debit += dec(poso)
        elif typ == CREDIT:
            self._bal -= dec(poso)
            self._total_credit += dec(poso)

    def line_final(self, per, typ, accode, acper=None):
        """Κλείσιμο εγγραφής"""
        # Θα πρέπει να υπάρχει ήδη τουλάχιστον μια γραμμή
        if self._nol == 0 or self.is_balanced:
            return
        delta = self._bal if typ == CREDIT else self._bal * -1
        self.line(per, typ, delta, accode, acper)
        assert self.is_balanced

    def line_final_auto(self, per, account, accountper=None):
        """Κλείσιμο εγγραφής με αυτόματη επιλογή χρέωσης/πίστωσης"""
        if self._nol == 0 or self.is_balanced:
            return
        if self._bal > 0:
            delta = self._bal
            trtyp = CREDIT
        else:
            delta = self._bal * -1
            trtyp = DEBIT
        self.line(per, trtyp, delta, account, accountper)
        assert self.is_balanced

    @property
    def journal(self):
        return self._journal

    @property
    def no(self):
        return self._no

    @property
    def date(self):
        return self._dat

    @property
    def par(self):
        return self._par

    @property
    def per(self):
        return self._per

    @property
    def total_debit(self):
        return self._total_debit

    @property
    def total_credit(self):
        return self._total_credit

    @property
    def ypoloipo(self):
        return self._bal

    @property
    def is_balanced(self):
        if self._nol < 2:  # Πρέπει να υπάρχουν τουλάχιστον δύο γραμμές
            return False
        if self._bal == 0:
            return True
        else:
            return False

    def kartella(self, lmos):
        lines_found = []
        for line in self._lns:
            if line.code == lmos:
                lines_found.append(line)
        return lines_found

    def __repr__(self):
        # status = 'Ισοσκελισμένο' if self.is_balanced else 'Ατελές'
        # ast = '%s %s %s %s (κατάσταση άρθρου: %s)\n'
        # atx = ast % (self._no, self._dat, self._par, self._per, status)
        ast = '%1s %5s %10s %s %s\n'
        atx = ast % (self._journal, self._no, self._dat, self._par, self._per)
        for lin in self._lns:
            atx += '  %s\n' % lin
        return atx


class Ledger():
    """Λογιστικό βιβλίο"""

    def __init__(self, data=None):
        self._trans = []  # Λίστα με λογιστικά άρθρα
        self._counter = 0  # Αριθμός λογιστικών άρθρων
        self._lmoi = {}

    def add(self, transaction):
        if not transaction.is_balanced:
            raise TransException('Not Valid transaction %s' % transaction)
        num = self._counter + 1
        transaction._no = num
        self._trans.append(transaction)
        self._counter = num
        for line in transaction._lns:
            self._lmoi[line.code] = self._lmoi.get(line.code, dec(0))
            self._lmoi[line.code] += line.ypo

    def to_json(self, file):
        dat = []
        for elm in self._trans:
            dat.append(elm.to_dict)
        with gzip.open(file, 'wb') as fil:
            fil.write(json.dumps(dat).encode('utf_8'))

    def from_json(self, file):
        dat = []
        with gzip.open(file, 'rb') as fil:
            dat = json.loads(fil.read().decode('utf_8'))
        for elm in dat:
            self.add(Tran('', '', '', dic=elm))

    def isozygio(self, apo=None, eos=None, journal=None):
        # apo = apo if apo else '1000-01-01'
        # eos = eos if eos else '9999-12-31'
        dacc = {}
        counter = 0
        for tran in self._trans:
            if journal:
                if tran.journal != journal:
                    continue
            if apo and eos:
                if not apo <= tran.date <= eos:
                    continue
            counter += 1
            for lin in tran._lns:
                # for code in lin.levels_tags:
                code = lin.code
                dacc[code] = dacc.get(code, {'xr': dec(0),
                                             'pi': dec(0),
                                             'yp': dec(0)})
                dacc[code]['xr'] += lin.xre
                dacc[code]['pi'] += lin.pis
                dacc[code]['yp'] += lin.ypo
        fin = {}
        txr = tpi = typ = dec(0)
        for key in dacc:
            lvls = levels(key)
            fin[key] = dacc[key]
            txr += dacc[key]['xr']
            tpi += dacc[key]['pi']
            typ += dacc[key]['yp']
            for lvl in lvls:
                fin[lvl] = fin.get(lvl, {'xr': dec(0),
                                         'pi': dec(0),
                                         'yp': dec(0)})
                fin[lvl]['xr'] += dacc[key]['xr']
                fin[lvl]['pi'] += dacc[key]['pi']
                fin[lvl]['yp'] += dacc[key]['yp']
        fin['t'] = {'xr': txr, 'pi': tpi, 'yp': typ}
        return fin, counter

    def isozygio_print(self, apo=None, eos=None, journal=None):
        dat, counter = self.isozygio(apo, eos, journal)
        ast = '%-15s %13s %13s %13s'
        print('Ισοζύγιο απο %s έως %s' % (apo, eos))
        for lmo in sorted(dat):
            print(ast % (lmo, dat[lmo]['xr'], dat[lmo]['pi'], dat[lmo]['yp']))
        print('Συνολικές εγγραφές περιόδου: %s' % counter)

    def transfer(self, date, lapo, lse, poso, journal=2):
        """Μετάφορά ποσού από ένα λογαριασμό σε άλλο"""
        par = 'Λ.Εγγρ.'
        per = 'Μεταφορά από %s σε %s' % (lapo, lse)
        tra = Tran(date, par, per, journal)
        tra.line('', CREDIT, poso, lapo)
        tra.line('', DEBIT, poso, lse)
        self.add(tra)

    def kleisimo_lmoy(self, date, lmos, lmosm, journal=2):
        """Μεταφορά υπολοίπου λογαριασμού σε λ/μο lmosm"""
        ypol = self.ypoloipo(lmos)
        if ypol == 0:
            return
        par = 'Λ.Εγγρ.'
        per = 'Μεταφορά από %s σε %s' % (lmos, lmosm)
        tra = Tran(date, par, per, journal)
        if ypol < 0:
            tra.line('', DEBIT, ypol * dec(-1), lmos)
            tra.line('', CREDIT, ypol * dec(-1), lmosm)
        else:
            tra.line('', CREDIT, ypol, lmos)
            tra.line('', DEBIT, ypol, lmosm)
        self.add(tra)

    def kleisimo_lmon(self, date, omada, lmos, antithetos=None, journal=2):
        """Κλείσιμο υπολοίπων ομάδας λογαριασμών"""
        found = []
        tposo = dec(0)
        for almo in self._lmoi:
            if almo.startswith(omada):
                if self.ypoloipo(almo) != 0:
                    found.append(almo)
                    tposo += self.ypoloipo(almo)
        print(found)
        if not found:
            return
        tra = Tran(date, 'Λογ.Εγγρ.', 'Κλείσιμο υπολοίπων', journal)
        if antithetos:
            if lmos == antithetos:
                return
            if tposo > 0:
                trtyp = CREDIT
            else:
                tposo = tposo * -1
                trtyp = DEBIT
            tra.line('', trtyp, tposo, antithetos)
        else:
            for lmo in found:
                if lmo == lmos:
                    continue
                poso = self.ypoloipo(lmo)
                if poso > 0:
                    trtyp = CREDIT
                else:
                    poso = poso * -1
                    trtyp = DEBIT
                tra.line('', trtyp, poso, lmo)
        tra.line_final_auto('', lmos)
        if tra.is_balanced:
            self.add(tra)

    def ypoloipo(self, lmos):
        return self._lmoi.get(lmos, dec(0))

    def open_accounts(self, acc):
        """Λίστα με ανοικτούς λογαριασμούς που μοιάζουν με τον acc"""
        promitheftes = []
        for lmo in self._lmoi:
            if lmo.startswith(acc):
                if self.ypoloipo(lmo) != 0:
                    promitheftes.append(lmo)
        return promitheftes

    def kartella(self, lmos):
        ast = '%1s %-10s %-5s %-15s %12s %12s'
        total_found = []
        for tran in self._trans:
            total_found += tran.kartella(lmos)
        for elm in sorted(total_found, key=lambda x: x.date):
            print(ast % (elm.journal, elm.date, elm.no, elm.par,
                         elm.xre, elm.pis))

    def se_apotelesmata(self, etos):
        DATE = '%s-12-31' % etos
        self.kleisimo_lmon(DATE, APOTH, APOTELESMATA, journal=3)
        self.kleisimo_lmon(DATE, EJODA, APOTELESMATA, journal=3)
        self.kleisimo_lmon(DATE, ESODA, APOTELESMATA, journal=3)
        self.kleisimo_lmon(DATE, FPA, FPAF, journal=3)

    def __repr__(self):
        ast = ''
        for tran in self._trans:
            ast += '%s\n' % tran
        return ast


def polee(date, par, ajia13, ajia24, pelafm, pelnam=None):
    """Πωλήσεις εμπορευμάτων εσωτερικού"""
    tra = Tran(date, par, 'Πωλήσεις χονδρικής εσωτερικού')
    if ajia13 != 0:
        tra.line('', CREDIT, ajia13, '70.00.7013', 'Πωλήσεις εμ/των ΦΠΑ 13%')
        fpa13 = dec(ajia13 * .13)
        tra.line('', CREDIT, fpa13, '54.00.7013', 'ΦΠΑ Πωλήσεων 13%')
    if ajia24 != 0:
        tra.line('', CREDIT, ajia24, '70.00.7024', 'Πωλήσεις εμ/των ΦΠΑ 24%')
        fpa24 = dec(ajia24 * .24)
        tra.line('', CREDIT, fpa24, '54.00.7024', 'ΦΠΑ Πωλήσεων 24%')
    pellmo = '30.00.%s' % pelafm
    tra.line_final('', DEBIT, pellmo, pelnam)
    return tra


def polli(date, par, ajia13, ajia24):
    """Πωλήσεις λιανικής εσωτερικού"""
    tra = Tran(date, par, 'Πωλήσεις λιανικής μηχανη 1')
    if ajia13 != 0:
        tra.line('', CREDIT, ajia13, '70.01.7013', 'Πωλήσεις Λιαν. ΦΠΑ 13%')
        fpa13 = dec(ajia13 * .13)
        tra.line('', CREDIT, fpa13, '54.00.7013', 'ΦΠΑ Πωλήσεων 13%')
    if ajia24 != 0:
        tra.line('', CREDIT, ajia24, '70.01.7024', 'Πωλήσεις Λιαν. ΦΠΑ 24%')
        fpa24 = dec(ajia24 * .24)
        tra.line('', CREDIT, fpa24, '54.00.7024', 'ΦΠΑ Πωλήσεων 24%')
    tra.line_final('', DEBIT, '38.00.00', 'Ταμείο')
    return tra


def plipro(date, par, proafm, poso):
    lmopro = '50.00.%s' % proafm
    tra = Tran(date, par, 'Εναντι λογαριασμού')
    tra.line('', DEBIT, poso, lmopro)
    tra.line_final('', CREDIT, '38.00.00', 'Ταμείο')
    return tra


def ageee(date, par, ajia13, ajia24, proafm, pronam=None):
    """Αγορές εμπορευμάτων εσωτερικού"""
    tra = Tran(date, par, 'Αγορές εμπορευμάτων εσωτερικού')
    if ajia13 != 0:
        tra.line('', DEBIT, ajia13, '20.00.2013', 'Αγορές εμ/των ΦΠΑ 13%')
        fpa13 = dec(ajia13 * .13)
        tra.line('', DEBIT, fpa13, '54.00.2013', 'ΦΠΑ Αγορών 13%')
    if ajia24 != 0:
        tra.line('', DEBIT, ajia24, '20.00.7024', 'Αγορές εμ/των ΦΠΑ 24%')
        fpa24 = dec(ajia24 * .24)
        tra.line('', DEBIT, fpa24, '54.00.2024', 'ΦΠΑ Αγορών 24%')
    prolmo = '50.00.%s' % proafm
    tra.line_final('', CREDIT, prolmo, pronam)
    return tra


def ejoda(date, par, ajia0, ajia13, ajia24, proafm, pronam=None):
    tra = Tran(date, par, 'Έξοδα χρήσης')
    if ajia0 != 0:
        tra.line('', DEBIT, ajia13, '64.00.6000', 'Έξοδα χωρίς ΦΠΑ')
    if ajia13 != 0:
        tra.line('', DEBIT, ajia13, '64.00.6013', 'Έξοδα με ΦΠΑ 13%')
        fpa13 = dec(ajia13 * .13)
        tra.line('', DEBIT, fpa13, '54.00.2913', 'ΦΠΑ εξόδων 13%')
    if ajia24 != 0:
        tra.line('', DEBIT, ajia24, '64.00.6024', 'Έξοδα με ΦΠΑ 24%')
        fpa24 = dec(ajia24 * .24)
        tra.line('', DEBIT, fpa24, '54.00.2924', 'ΦΠΑ εξόδων 24%')
    prolmo = '50.00.%s' % proafm
    tra.line_final('', CREDIT, prolmo, pronam)
    return tra


def generate_transactions(number=100, year=2017):
    import random
    from datetime import datetime

    def rdate(etos):
        try:
            dnum = random.randint(1, 365)
            rda = datetime.strptime('{} {}'.format(dnum, etos), '%j %Y')
            return rda.date().isoformat()
        except ValueError:
            rdate(etos)

    # print('generate_transactions started')
    rdates = []
    for i in range(number):
        rdates.append(rdate(year))
    rdates.sort()
    ledger = Ledger()
    for i in range(number):
        typ = random.randint(1, 7)
        date = rdates[i]
        par = 'ΤΔΑ%s' % (i + 1)
        p13 = random.randint(0, 100)
        p24 = random.randint(0, 100)
        if p13 + p24 == 0:
            p13 = 1
        afm = str(random.randint(999999910, 999999999))
        if typ in (1, 7):
            ledger.add(polee(date, par, p13 * 1.4, p24 * 1.4, afm))
        elif typ == 2:
            ledger.add(ageee(date, par, p13, p24, afm))
        elif typ == 3:
            par = 'Z%s' % (i + 1)
            ledger.add(polli(date, par, p13, p24))
        elif typ == 4:  # Πληρωμή πελατών
            pels = ledger.open_accounts('30.00')
            if pels:
                ledger.kleisimo_lmoy(date, random.choice(pels), '38.00.00')
            else:
                ledger.add(polee(date, par, p13, p24, afm))
        elif typ == 5:  # Πληρωμή προμηθευτών
            proms = ledger.open_accounts('50.00')
            if proms:
                ledger.kleisimo_lmoy(date, random.choice(proms), '38.00.00')
            else:
                ledger.add(ageee(date, par, p13, p24, afm))
        elif typ == 6:
            p00 = random.randint(0, 100)
            ledger.add(ejoda(date, par, p00, p13, p24, afm))
        else:
            pass
    # print('generate_transactions finished')
    return ledger


if __name__ == '__main__':
    ledger = generate_transactions(10)
    # ledger.kleisimo_lmoy('2017-12-31', '38.00.00', '38.03.00')
    # ledger.isozygio_print('2017-01-01', '2017-12-31')
    # ledger.kartella('38.00.00')
    # print(ledger)
    # print(ledger.ypoloipo('38.00.00'))
    print(ledger.to_json)
