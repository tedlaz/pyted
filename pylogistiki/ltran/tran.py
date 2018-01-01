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
ACCOUNT_TYPES = {'1': ['Πάγια', 'Ισολογισμός', 'Ενεργητικό'],
                 '2': ['Αποθέματα', 'Ισολογισμός', 'Ενεργητικό'],
                 '3': ['Απαιτήσεις', 'Ισολογισμός', 'Ενεργητικό'],
                 '38': ['Ταμιακά διαθέσιμα'],
                 '4': ['Κεφάλαιο', 'Ισολογισμός', 'Παθητικό'],
                 '5': ['Υποχρεώσεις', 'Ισολογισμός', 'Παθητικό'],
                 '54.00': ['ΦΠΑ'],
                 '6': ['Εξοδα', 'Αποτελέσματα'],
                 '7': ['Εσοδα', 'Αποτελέσματα'],
                 '8': ['Ανόργανα']
                 }
ACCOUNT_SPLITTER = '.'
DEBIT, CREDIT = 1, 2


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
        return self._nam if self._nam else '# Λείπει Όνομα λ/μού !!! #'

    @property
    def tags(self):
        rlist = []
        for atyp in ACCOUNT_TYPES:
            if self._cod.startswith(atyp):
                rlist += ACCOUNT_TYPES[atyp]
        return rlist

    @property
    def levels(self):
        arlev = self._cod.split(ACCOUNT_SPLITTER)
        rlist = [self._cod[0]]  # Βάζουμε την ομάδα
        for i, _ in enumerate(arlev):
            rlist.append('.'.join(arlev[:i + 1]))
        return rlist

    def __repr__(self):
        return '%-15s %s (%s)' % (self._cod, self.name, self.tags)


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
    def date(self):
        return self._parent.date if self._parent else '??? date ???'

    @property
    def par(self):
        return self._parent.par if self._parent else '??? par ???'

    @property
    def per(self):
        return self._parent.per if self._parent else '??? per ???'

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
    def levels(self):
        return self._acc.levels

    def __repr__(self):
        ast = '%4s %-90s %-20s %12s %12s'
        return ast % (self._no, self._acc, self._pel, self.xre, self.pis)


class Tran():
    """Λογιστικό άρθρο"""

    def __init__(self, date, par, per):
        self._no = 0
        self._dat = date  # Ημερομηνία εγγραφής
        self._par = par  # Παραστατικό
        self._per = per  # Περιγραφή
        self._lns = []  # Λίστα με αναλυτικές γραμμές
        self._nol = 0  # Αριθμός γραμμών
        self._total_debit = dec(0)  # συνολική χρέωση
        self._total_credit = dec(0)  # συνολική πίστωση
        self._bal = dec(0)  # Υπόλοιπο (χρεώσεις - πιστώσεις)

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
        # Θα πρέπει να υπάρχει ήδη τουλάχιστον μια γραμμή
        assert self._nol >= 1
        delta = self._bal if typ == CREDIT else self._bal * -1
        self.line(per, typ, delta, accode, acper)
        assert self.is_balanced

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
        status = 'Ισοσκελισμένο' if self.is_balanced else 'Ατελές'
        ast = '%s %s %s %s (κατάσταση άρθρου: %s)\n'
        atx = ast % (self._no, self._dat, self._par, self._per, status)
        for lin in self._lns:
            atx += '  %s\n' % lin
        return atx


class Ledger():
    """Λογιστικό βιβλίο"""

    def __init__(self):
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

    def isozygio(self, apo=None, eos=None):
        # apo = apo if apo else '1000-01-01'
        # eos = eos if eos else '9999-12-31'
        dacc = {}
        counter = 0
        for tran in self._trans:
            if apo and eos:
                if not apo <= tran.date <= eos:
                    continue
            counter += 1
            for lin in tran._lns:
                for code in lin.levels:
                    dacc[code] = dacc.get(code, {'xr': dec(0),
                                                 'pi': dec(0),
                                                 'yp': dec(0)})
                    dacc[code]['xr'] += lin.xre
                    dacc[code]['pi'] += lin.pis
                    dacc[code]['yp'] += lin.ypo
        return dacc, counter

    def kleisimo_lmoy(self, date, lmos, lmosm):
        """Μεταφορά υπολοίπου λογαριασμού σε λ/μο lmosm"""
        ypol = self.ypoloipo(lmos)
        if ypol == 0:
            return
        per = 'Μεταφορά από %s σε %s' % (lmos, lmosm)
        tra = Tran(date, per, per)
        if ypol < 0:
            tra.line('', DEBIT, ypol * dec(-1), lmos)
            tra.line('', CREDIT, ypol * dec(-1), lmosm)
        else:
            tra.line('', CREDIT, ypol, lmos)
            tra.line('', DEBIT, ypol, lmosm)
        self.add(tra)

    def isozygio_print(self, apo=None, eos=None):
        dat, counter = self.isozygio(apo, eos)
        ast = '%-15s %10s %10s %10s'
        print('Ισοζύγιο απο %s έως %s' % (apo, eos))
        for lmo in sorted(dat):
            print(ast % (lmo, dat[lmo]['xr'], dat[lmo]['pi'], dat[lmo]['yp']))
        print('Συνολικές εγγραφές περιόδου: %s' % counter)

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
        ast = '%-10s %-5s %-15s %12s %12s'
        total_found = []
        for tran in self._trans:
            total_found += tran.kartella(lmos)
        for elm in sorted(total_found, key=lambda x: x.date):
            print(ast % (elm.date, elm.no, elm.par, elm.xre, elm.pis))

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


def generate_transactions(number=100):
    import random
    from datetime import datetime

    def rdate(year):
        try:
            dnum = random.randint(1, 365)
            rda = datetime.strptime('{} {}'.format(dnum, year), '%j %Y')
            return rda.date().isoformat()
        except ValueError:
            rdate(year)

    rdates = []
    for i in range(number):
        rdates.append(rdate(2017))
    rdates.sort()
    ledger = Ledger()
    for i in range(number):
        typ = random.randint(1, 5)
        date = rdates[i]
        par = 'ΤΔΑ%s' % (i + 1)
        p13 = random.randint(0, 100)
        p24 = random.randint(0, 100)
        if p13 + p24 == 0:
            p13 = 1
        afm = str(random.randint(999999910, 999999999))
        if typ == 1:
            ledger.add(polee(date, par, p13, p24, afm))
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
        else:
            pass
    return ledger


if __name__ == '__main__':
    ledger = generate_transactions(1000)
    ledger.kleisimo_lmoy('2017-12-31', '38.00.00', '38.03.00')
    ledger.isozygio_print('2017-01-01', '2017-12-31')

    # ledger.kartella('38.00.00')
    # print(ledger)
    print(ledger.ypoloipo('38.00.00'))
