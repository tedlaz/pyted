# *- coding: utf-8 -*

import decimal
import json


class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


def defaultencode(o):
    if isinstance(o, decimal.Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")


def dec(poso=0, decimals=2):
    def isNum(value):  # Einai to value arithmos, i den einai ?
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


KIN_CATEG = [ESODA, EJODA] = [7, 26]
KIN_CATEGP = {ESODA: u'Έσοδα', EJODA: u'Έξοδα'}
KIN_TYPES = [NORMAL, CREDIT] = ['normal', 'credit']
KIN_TYPESP = {NORMAL: u'Κανονικό', CREDIT: u'Πιστωτικό'}
KIN_PROEL = [ESOTERIKO, ENDOKINOTIKI, EJOTERIKO] = ['ell', 'eur', 'exo']
KIN_PROELP = {ESOTERIKO: u'Εσωτερικού',
              ENDOKINOTIKI: u'Ενδοκοινοτική',
              EJOTERIKO: u'Εξωτερικού'}


def findcode(code):
    '''
    Ψάχνει να βρεί τον πιο κοντινό λογαριασμό από τη λίστα lm
    '''
    codelen = len(code)
    ignorechar = '.'
    for i in reversed(range(codelen)):
        if code[i] == ignorechar:
            continue
        if code[:i + 1] in lm.keys():
            # return '%s -> %s' % (code[:i + 1], lm[code[:i + 1]])
            return '%s' % lm[code[:i + 1]]
    return ''

lm = {'2': u'Αποθέματα', '7': u'Πωλήσεις'}


class Kinisi():
    def __init__(self, cat, _id, dat, par, afm, per, typ=NORMAL, xor=ESOTERIKO):
        self._id = _id  # Κωδικός
        self.cat = cat  # Έσοδα ή έξοδα
        self.typ = typ  # Τύπος κίνησης (κανονική ή πιστωτική)
        self.xor = xor  # Εσωτερικού, Ενδοκοινοτική, Εξωτερικό
        self.dat = dat  # Ημερομηνία
        self.par = par  # Παραστατικό
        self.afm = afm  # ΑΦΜ Συμβαλλομένου
        self.per = per  # Περιγραφή
        self.lns = []  # Γραμμές
        self.tposo = dec(0)  # ΣΥΝΟΛΙΚΟ ΠΟΣΟ ΠΡΟ ΦΠΑ
        self.tfpa = dec(0)  # ΣΥΝΟΛΙΚΟΣ ΦΠΑ
        self.ttot = dec(0)  # ΤΕΛΙΚΟ ΠΟΣΟ ΜΕ ΦΠΑ

    def addLine(self, lmo, pfpa, poso):
        dposo = dec(poso)
        dpfpa = dec(dec(pfpa) / dec(100))
        if self.cat == ESODA:
            assert lmo[0] in '7'
        else:
            assert lmo[0] in '26'
        line = {}
        line['llmo'] = lmo
        line['pfpa'] = pfpa
        line['poso'] = dposo
        line['fpa'] = dec(dposo * dpfpa)
        self.tposo += dposo
        self.tfpa += line['fpa']
        self.ttot = self.tposo + self.tfpa
        self.lns.append(line)

    def todic(self):
        d = {}
        d['afm'] = self.afm
        d['cat_id'] = self.cat
        d['dat'] = self.dat
        d['id'] = self._id
        d['ori_id'] = self.xor
        d['per'] = self.per
        d['pli_id'] = 1
        d['pno'] = self.par
        d['typ_id'] = self.typ
        d['zlines'] = []
        for line in self.lns:
            d2 = {}
            d2['lm_id'] = line['llmo']
            d2['pfpa'] = line['pfpa']
            d2['val'] = line['poso']
            d2['fpa'] = line['fpa']
            d['zlines'].append(d2)
        return d

    def tojson(self):
        return json.dumps(self.todic(),
                          default=defaultencode,
                          ensure_ascii=False,
                          sort_keys=True,
                          indent=2,
                          separators=(',', ':'))

    def __str__(self):
        ast = u'αα          : %s\n' % self._id
        ast += u'Κατηγορία   : %s\n' % KIN_CATEGP[self.cat]
        ast += u'τύπος       : %s\n' % KIN_TYPESP[self.typ]
        ast += u'Προέλευση   : %s\n' % KIN_PROELP[self.xor]
        ast += u'Ημ/νια      : %s\n' % self.dat
        ast += u'Παραστατικό : %s\n' % self.par
        ast += u'ΑΦΜ         : %s\n' % self.afm
        ast += u'Περιγραφή   : %s\n' % self.per
        ast += u'Καθαρή αξία : %12s\n' % self.tposo
        ast += u'    ΦΠΑ     : %12s\n' % self.tfpa
        ast += u'  Σύνολο    : %12s\n' % (self.tposo + self.tfpa)
        ''''
        for i, l in enumerate(self.lns):
            lmo, _ = self.mlmo(l['llmo'], l['pfpa'])
            ast += u'%s %s %s %s %s\n' % (i+1, lmo, l['pfpa'], l['poso'], l['fpa'])
        '''
        return ast + self.make_Logistiki()

    def mlmo(self, kode, fpa):
        '''
        ΔΗΜΙΟΥΡΓΙΑ ΚΙΝΟΥΜΕΝΟΥ ΛΟΓΑΡΙΑΣΜΟΥ ΚΑΙ ΠΕΡΙΓΡΑΦΗΣ
        ΛΛ.ΛΛ.00.ΧΦΦ
        ΛΛ.ΛΛ = ΔΕΥΤΕΡΟΒΑΘΜΙΟΣ ΛΟΓΙΣΤΙΚΗΣ
        X = (0 = εσωτερικό, 1 = Ενδοκοινοτικό, 2 = Εξωτερικό)
        ΦΦ = Συντελεστής ΦΠΑ
        πχ 70.00.00.024
        '''
        proel = '%s' % KIN_PROEL.index(self.xor)
        if len(kode) == 5:
            if int(fpa) == 0:
                tlmo = '%s.00.%s0%s'
            else:
                tlmo = '%s.00.%s%s'
        else:
            if int(fpa) == 0:
                tlmo = '%s.%s0%s'
            else:
                tlmo = '%s.%s%s'  # Template για δημιουργία λογαριασμού
        clmo = tlmo % (kode, proel, fpa)
        plmo = findcode(clmo)
        xora = KIN_PROELP[self.xor]
        pfpa = 'χωρίς ΦΠΑ'
        if fpa > 0:
            pfpa = 'με ΦΠΑ %s%%' % fpa
        flmo = '%s %s %s' % (plmo, xora, pfpa)
        return clmo, flmo

    def mfpa(self, kode, fpa):
        '''
        ΔΗΜΙΟΥΡΓΙΑ ΚΙΝΟΥΜΕΝΟΥ ΛΟΓΑΡΙΑΣΜΟΥ ΦΠΑ ΚΑΙ ΠΕΡΙΓΡΑΦΗΣ
        54.00.ΛΛ.ΧΦΦ :
        ΛΛ = Πρωτοβάθμιος λογαριασμός,
        X = (0 = εσωτερικό, 1 = Ενδοκοινοτικό, 2 = Εξωτερικό)
        ΦΦ = Συντελεστής ΦΠΑ
        '''
        if fpa == 0:
            return '', ''
        cfpa = 'ΦΠΑ γιά %s %s %s%%' % (findcode(kode), KIN_PROELP[self.xor], fpa)
        proel = '%s' % KIN_PROEL.index(self.xor)
        lfpa = '54.00.%s.%s%s' % (kode[:2], proel, fpa)
        return lfpa, cfpa

    def todicl(self):
        if self.typ == NORMAL:
            synt1 = dec(1)
        else:
            synt1 = dec(-1)

        lg = {}
        lg['dat'] = self.dat
        lg['par'] = self.par
        lg['per'] = self.per
        lg['zlines'] = []
        for lin in self.lns:
            dlin = {}
            dlin['lmo'], dlin['per2'] = self.mlmo(lin['llmo'], lin['pfpa'])
            if self.cat == EJODA:
                dlin['xr'] = dec(lin['poso'] * synt1)
                dlin['pi'] = dec(0)
            else:
                dlin['xr'] = dec(0)
                dlin['pi'] = dec(lin['poso'] * synt1)
            lg['zlines'].append(dlin)

            if lin['pfpa'] != 0:
                dfpa = {}
                dfpa['lmo'], dfpa['per2'] = self.mfpa(lin['llmo'], lin['pfpa'])
                if self.cat == EJODA:
                    dfpa['xr'] = dec(lin['fpa'] * synt1)
                    dfpa['pi'] = dec(0)
                else:
                    dfpa['xr'] = dec(0)
                    dfpa['pi'] = dec(lin['fpa'] * synt1)
                lg['zlines'].append(dfpa)
        dtot = {}
        dtot['lmo'], dtot['per2'] = self.es_xora()
        if self.cat == EJODA:
            dtot['xr'] = dec(0)
            dtot['pi'] = dec(self.ttot * synt1)
        else:
            dtot['xr'] = dec(self.ttot * synt1)
            dtot['pi'] = dec(0)
        lg['zlines'].append(dtot)
        return lg

    def tojsonl(self):
        return json.dumps(self.todicl(),
                          default=defaultencode,
                          ensure_ascii=False,
                          sort_keys=True,
                          indent=2,
                          separators=(',', ':'))

    def es_xora(self):
        if self.cat == EJODA:
            if self.xor == ESOTERIKO:
                partn = '50.00.00.%s' % self.afm
                partp = u'Προμηθευτές εσωτερικού'
            elif self.xor == ENDOKINOTIKI:
                partn = '50.01.00.%s' % self.afm
                partp = u'Προμηθευτές ενδοκοινοτικοί'
            elif self.xor == EJOTERIKO:
                partn = '50.02.00.%s' % self.afm
                partp = u'Προμηθευτές εξωτερικού'
            else:
                partn = '50.99.99.%s' % self.afm
                partp = u'Προμηθευτές άγνωστοι'

        else:
            if self.xor == ESOTERIKO:
                partn = '30.00.00.%s' % self.afm
                partp = u'Πελάτες εσωτερικού'
            elif self.xor == ENDOKINOTIKI:
                partn = '30.01.00.%s' % self.afm
                partp = u'Πελάτες ενδοκοινοτικοί'
            elif self.xor == EJOTERIKO:
                partn = '30.02.00.%s' % self.afm
                partp = u'Πελάτες εξωτερικού'
            else:
                partn = '30.99.99.%s' % self.afm
                partp = u'Πελάτες άγνωστοι'
        return partn, partp

    def make_Logistiki(self):
        tline = '%-78s %12s %12s\n'
        st = tline % ('Lmos', 'Xreosi', 'Pistosi')
        # Έλεγχος κίνησης και αν είναι πιστωτική αλλάζουμε
        # τα πρόστιμα του άρθρου

        if self.typ == NORMAL:
            synt = dec(1)
        else:
            synt = dec(-1)

        for el in self.lns:

            lmos = '%s %s' % self.mlmo(el['llmo'], el['pfpa'])
            lfpa = '%s %s' % self.mfpa(el['llmo'], el['pfpa'])
            tposo = dec((self.tposo + self.tfpa) * synt)

            if el['pfpa'] != 0:
                fpa = dec(el['fpa'] * synt)
            else:
                fpa = 0

            if self.cat == EJODA:
                xreosi = dec(el['poso'] * synt)
                pistosi = dec(0)
                fpax = fpa
                fpap = ''
                tposox = ''
                tposop = tposo

            else:
                xreosi = dec(0)
                pistosi = dec(el['poso'] * synt)
                fpax = ''
                fpap = fpa
                tposox = tposo
                tposop = ''

            st += tline % (lmos, xreosi, pistosi)
            if lfpa != ' ':
                st += tline % (lfpa, fpax, fpap)
        partf = '%s %s' % (self.es_xora())
        st += tline % (partf, tposox, tposop)
        return st


if __name__ == "__main__":
    tr = Kinisi(EJODA, 1, '2016-09-01', u'ΤΔΑ345', '046949583',
                "Αγορά 1", CREDIT, ESOTERIKO)
    tr.addLine('20.01', 23, 100.0)
    tr.addLine('24.01', 13, 100.0)
    # print(tr)

    # print(tr.mlmo('20', 23))
    # print(tr.make_Logistiki())

    tr2 = Kinisi(ESODA, 2, '2016-09-01', u'ΤΔΑ550', '046949947',
                 "Πώληση 1",  NORMAL, ESOTERIKO)
    tr2.addLine('70.00.34', 24, 100.36)
    tr2.addLine('71.00', 13, 100.12)
    tr2.addLine('73.00', 24, 100.0)
    print(tr2)
    print('To Dic', tr2.todic())
    print('To Jsonl', tr2.tojsonl())
    print('To Json', tr2.tojson())
    # print(tr2.make_Logistiki())
    # Αγορά απο προμηθευτή εσωτερικού Λάζαρο των εξής :
    # Εμπορεύματα με φπα 13% 1400 ευρώ
    # Πρώτες ύλες με φπα 13% 150 ευρώ
    # Πρώτες ύλες με φπα 23% 200 ευρώ
    # Πιστωτικό τιμολόγιο επιστροφής σε προμηθευτή εσωτερικού Λάζαρο των εξής:
    # Εμπορεύματα με φπα 13% 54 ευρώ
    # print(findcode('72.00'))
