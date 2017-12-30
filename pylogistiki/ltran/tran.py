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
    def name(self):
        return self._nam if self._nam else '# Λείπει Όνομα λ/μού !!! #'

    @property
    def code(self):
        return self._cod

    @property
    def tags(self):
        rlist = []
        for atyp in ACCOUNT_TYPES:
            if self._cod.startswith(atyp):
                rlist += ACCOUNT_TYPES[atyp]
        return rlist

    @property
    def account_levels(self):
        arlev = self._cod.split(ACCOUNT_SPLITTER)
        rlist = [self._cod[0]]  # Βάζουμε την ομάδα
        for i, _ in enumerate(arlev):
            rlist.append('.'.join(arlev[:i + 1]))
        return rlist

    def __repr__(self):
        return '%s %s (%s)' % (self._cod, self.name, self.tags)


class TransLine():
    """Λογιστική εγγραφή"""

    def __init__(self, num, perigrafi, typ, poso, acccode, accper=None):
        assert typ in (CREDIT, DEBIT)
        self._no = num  # Αριθμός γραμμής
        self._acc = Account(acccode, accper)  # Λογαριασμός
        self._pel = perigrafi  # Περιγραφή
        self._typ = typ  # 1 για χρέωση 2 για πίστωση
        self._val = poso  # Ποσό

    @property
    def xre(self):
        return self._val if self._typ == CREDIT else 0

    @property
    def pis(self):
        return self._val if self._typ == DEBIT else 0

    @property
    def ypo(self):
        return self.xre - self.pis

    def __repr__(self):
        ast = '%5s %-80s %-20s %12s %12s'
        xre = self._val if self._typ == DEBIT else 0
        pis = self._val if self._typ == CREDIT else 0
        return ast % (self._no, self._acc, self._pel, xre, pis)


class Trans():
    """Λογιστικό άρθρο"""

    def __init__(self, date, par, per):
        self._no = 0
        self._dat = date  # Ημερομηνία εγγραφής
        self._par = par  # Παραστατικό
        self._per = per  # Περιγραφή
        self._lns = []  # Λίστα με αναλυτικές γραμμές
        self._nol = 0  # Αριθμός γραμμών
        self._total_debit = 0  # συνολική χρέωση
        self._total_credit = 0  # συνολική πίστωση
        self._bal = 0  # Υπόλοιπο (χρεώσεις - πιστώσεις)

    def line(self, per, typ, poso, accode, acper=None):
        self._lns.append(TransLine(self._nol + 1, per, typ, poso,
                                   accode, acper))
        self._nol += 1
        if typ == DEBIT:
            self._bal += poso
            self._total_debit += poso
        elif typ == CREDIT:
            self._bal -= poso
            self._total_credit += poso

    def line_final(self, per, typ, accode, acper=None):
        # Θα πρέπει να υπάρχει ήδη τουλάχιστον μια γραμμή
        assert self._nol >= 1
        delta = self._bal if typ == CREDIT else self._bal * -1
        self.line(per, typ, delta, accode, acper=None)
        assert self.is_balanced

    @property
    def total_debit(self):
        return self._total_debit

    @property
    def total_credit(self):
        return self._total_credit

    @property
    def is_balanced(self):
        if self._nol < 2:  # Πρέπει να υπάρχουν τουλάχιστον δύο γραμμές
            return False
        if self._bal == 0:
            return True
        else:
            return False

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

    def add_trans(self, transaction):
        if not transaction.is_balanced:
            raise TransException('Not Valid transaction %s' % transaction)
        num = self._counter + 1
        transaction._no = num
        self._trans.append(transaction)
        self._counter = num

    def isozygio(self):
        for tran in self._trans:
            for account in tran._lns:
                print(account)

    def __repr__(self):
        ast = ''
        for tran in self._trans:
            ast += '%s\n' % tran
        return ast


if __name__ == '__main__':
    ac = Account('54.00.00', 'ΦΠΑ δοκιμαστικό')
    tr1 = Trans('2017-01-01', 'ΤΠΥ2345', 'Δοκιμαστικό')
    tr1.line('', 1, 10, '20.00', 'sdfsf')
    tr1.line('', 1, 2, '54.00', 'ΦΠΑ')
    tr1.line_final('', 2, '50.00', 'Προμηθευτές')
    ledger = Ledger()
    ledger.add_trans(tr1)
    tr2 = Trans('2017-01-02', 'Αποδ23', 'Δοκιμαστικό')
    tr2.line('', 1, 12, '50.00')
    tr2.line('', 2, 12, '38.00', 'Ταμείο')
    ledger.add_trans(tr2)
    print(ledger)
    print(ledger.isozygio())
