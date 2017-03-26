# -*- coding: utf-8 -*-

from dec import dec


MISTHOS, IMER, OROM = range(3)
mtyp = {0: 'Μισθωτός', 1: u'Ημερομίσθιος', 2: u'Ωρομίσθιος'}

class Mis():
    '''
    Υπολογισμός μισθοδοσίας
    '''

    def __init__(self):
        self.meres_mina_misthotoy = dec(25, 0)
        self.meres_mina_imeromisthioy = dec(26, 0)
        self.meres_bdomadas = dec(6, 0)
        self.ores_bdomadas = dec(40, 0)
        self.synt_nyxta = dec(0.25)
        self.synt_argia = dec(0.75)

    @property
    def synt_oromisthioy(self):
        return dec(self.meres_bdomadas / self.ores_bdomadas, 6)

    @property
    def synt_apodoxon_misthotoy(self):
        return dec(self.meres_mina_misthotoy / self.meres_bdomadas, 6)

    @property
    def synt_apodoxon_imeromisthioy(self):
        return dec(self.meres_mina_imeromisthioy / self.meres_bdomadas, 6)

    def misthos(self, fullmisthos, ores_bdomada=40):
        return dec(dec(fullmisthos) * dec(ores_bdomada) / self.ores_bdomadas)

    def imeromisthio_meriko(self, fullImeromisthio, ores):
        return dec(dec(fullImeromisthio) * dec(ores) / self.ores_bdomadas)

    def imeromisthio_from_misthos(self, misthos, ores=40):
        return dec(dec(misthos) / self.meres_mina_misthotoy * dec(ores) / self.ores_bdomadas)

    def oromisthio_from_misthos(self, misthos):
        return dec(self.imeromisthio_from_misthos(misthos) * self.synt_oromisthioy)

    def oromisthio(self, imeromisthio):
        return dec(dec(imeromisthio) * self.synt_oromisthioy)

    def misthos_from_imsthio_ores_bdom(self, imsthio, ores=40, misthotos=True):
        '''
        Υπολογισμός μισθού από ημερομίσθιο και ώρες εργασίας ανά βδομάδα
        Χρήσιμο για την υποβολή προγράμματος εργασίας στο sepe
        '''
        oromisthio = self.oromisthio(imsthio)
        if misthotos:
            return dec(oromisthio * dec(ores) * self.synt_apodoxon_misthotoy)
        else:
            return dec(oromisthio * dec(ores) * self.synt_apodoxon_imeromisthioy)

    def calc_ika(self, poso, pika, pikae):
        '''
        Υπολογισμός κρατήσεων ΙΚΑ
        '''
        ika = dec(dec(poso) * dec(pika, 4))
        ikaer = dec(dec(poso) * dec(pikae, 4))
        ikaet = ika - ikaer
        return ika, ikaer, ikaet

    def calc_foro(self, poso):
        '''
        Υπολογισμός φόρου εισοδήματος και ειδικού επιδόματος αλληλεγγύης
        '''
        foro = dec(dec(poso) * dec(.22))  # Φόρος εισοδήματος
        eeal = dec(dec(poso) * dec(.1))  # Ειδικό επίδομα αλληλεγγύης
        return foro, eeal

    def calc_tac(self, ft):
        '''
        Υπολογισμός τακτικών αποδοχών
        mergas : Ημέρες κανονικής εργασίας
        madeia : Ημέρες σε κανονική (πληρωμένη) άδεια
        onyxta : Νυχτερινές ώρες εργασίας για προσαύξηση 25%
        oargia : Ώρες Κυρακής ή Αργίας για προσαύξηση 75%
        margia : Μέρες Κυριακών/αργιών για προσαύξηση 75%
        '''
        at = {}  #  Τακτικές αποδοχές
        at['mergas'] = dec(ft['dpar']['dtac'].get('mergas', 0))
        at['madeia'] = dec(ft['dpar']['dtac'].get('madeia', 0))
        at['tmeres'] = at['mergas'] + at['madeia']
        at['onyxta'] = dec(ft['dpar']['dtac'].get('onyxta', 0))
        at['oargia'] = dec(ft['dpar']['dtac'].get('oargia', 0))
        at['margia'] = dec(ft['dpar']['dtac'].get('margia', 0))

        pnyxta = dec(dec(ft['oromist']) * self.synt_nyxta, 6)  # Συντελεστής ωρών νύχτας
        pargio = dec(dec(ft['oromist']) * self.synt_argia, 6)  # Συντελεστής ωρών αργίας
        pargim = dec(dec(ft['imsthio']) * self.synt_argia, 6)  # Συντελεστής ημερών αργίας

        at['ap_normal'] = dec(dec(ft['imsthio']) * dec(at['tmeres']))
        at['ap_onyxta'] = dec(pnyxta * dec(at['onyxta']))
        at['ap_oargia'] = dec(pargio * dec(at['oargia']))
        at['ap_margia'] = dec(pargim * dec(at['margia']))
        at['ap_per'] = at['ap_normal'] + at['ap_onyxta'] + at['ap_oargia'] + at['ap_margia']
        ika = self.calc_ika(at['ap_per'], ft['pika'], ft['pikae'])
        at['ika'] = ika[0]
        at['ikaer'] = ika[1]
        at['ikaet'] = ika[2]
        at['ap_forol'] = at['ap_per'] - at['ikaer']
        ft['at'] = at

    def calc_ype(self, fyp):
        pass

    def calc_astheneies(self, fa):
        '''
        Υπολογισμός αποδοχών ασθενείας
        Παράμετροι εισόδου:
        imsthio : Hμερομίσθιο
        dapo    : Ημερομηνία ασθένειας από
        deos    : Ημερομηνία ασθένειας έως
        masl3   : Μέρες ασθένειας <= 3
        masm3   : Μέρες ασθένειας > 3
        mas0    : Μέρες ασθένειας χωρίς αποδοχές
        eas     : Επίδομα ασθένειας ΙΚΑ
        Παράμετροι εξόδου:
        apl3 : Αποδοχές ασθένειας <=3
        apm3 : Αποδοχές ασθενείας > 3
        '''
        # 'dast': {'dapo': DDDD, 'deos': DDDD, 'masl3': xx, 'masm3': xx, 'mas0':xx, 'eas': xx }
        d100 = dec(100)
        aa = []
        aat = {'ap_per': 0, 'ika': 0, 'ikaer': 0, 'ikaet': 0 , 'ap_totf': 0,
               'ap_forol': 0, 'eas':0, 'isfas': 0}
        for pa in fa['dpar']['dast']:
            d = {}
            d['dapo'] = pa['dapo']
            d['deos'] = pa['deos']
            d['masl3'] = dec(pa.get('masl3', 0))
            d['masm3'] = dec(pa.get('masm3', 0))
            d['mas0'] = dec(pa.get('mas0', 0))
            d['eas'] = dec(pa.get('eas', 0))
            d['ap_l3'] = dec(dec(fa['imsthio']) * d['masl3'] / dec(2))
            d['ap_m3'] = dec(dec(fa['imsthio']) * d['masm3'])
            d['ap_per'] = d['ap_l3'] + d['ap_m3']
            ika = self.calc_ika(d['ap_per'], fa['pika'], fa['pikae'])
            ikaeas = self.calc_ika(d['eas'], fa['pika'], fa['pikae'])
            d['ika'] = ika[0]
            d['ikaer'] = ika[1]
            d['ikaet'] = ika[2]
            d['isfas'] = ikaeas[1]
            d['ap_forol'] = dec(d['ap_per'] + ikaeas[1] - d['ikaer']) - dec(d['eas'])
            d['ap_totf'] = d['ap_per'] - d['eas']
            aa.append(d)
            aat['ap_per'] += d['ap_per']
            aat['ika'] += d['ika']
            aat['ikaer'] += d['ikaer']
            aat['ikaet'] += d['ikaet']
            aat['ap_totf'] += d['ap_totf']
            aat['ap_forol'] += d['ap_forol']
            aat['eas'] += d['eas']
            aat['isfas'] += d['isfas']
        fa['aa'] = aa
        fa['aat'] = aat


    def calc1(self, etyp, apod, dpar, dika):
        '''
        Υπολογισμός μισθοδοσίας
        Παράμετροι εισόδου:
        etyp : Τύπος εργαζομένου (Μισθωτός, ήμερομίσθιος, ωρομίσθιος)
        apod : Ανάλογα με τον τύπο εργαζομένου (Μισθός, Ημερομίσθιο, Ωρομίσθιο)
        dpar : Παρουσίες εργαζομένου που αναλύονται ως εξής:
               1.dtac: Τακτικές παρουσίες.Σε κάθε περίοδο έχουμε το πολύ μία φορά
                 δεδομένα αυτής της κατηγορίας.
                 1.tmeres : Ημέρες εργασίας
                 2.madeia : Ημέρες κανονικής αδείας (με αποζημίωση)
                 3.onyxta : Ώρες νυχτερινές μόνο προσαύξηση 25%
                 4.oargia : Ώρες αργίας μόνο προσαύξηση 75%
                 5.margia : Μέρες αργίας μόνο προσαύξηση 75% (Πρέπει να
                            συνπεριλαμβάνονται και στο tmeres)
               2.dype.Υπερωρίες. Χρειάζεται παραπάνω ανάλυση.
                 ???
               3.dast: Ασθένειες. Σε μιά περίοδο μπορεί να υπάρχουν πάνω από
                 μία φορά ασθένειες οι οποίες αποτυπώνονται ξεχωριστά.
                 1.dapo  : Ημερομηνία ασθένειας από
                 2.deos  : Ημερομηνία ασθένειας έως
                 3.masl3 : Μέρες ασθένειας <= 3
                 4.masm3 : Μέρες ασθένειας > 3
                 5.mas0  : Μέρες ασθένειας χωρίς αποδοχές
                 6.eas   : Επίδομα ασθένειας ΙΚΑ
               Μπορεί να υπάρχουν και οι τρείς περιπτώσεις μπορεί και μόνο μία
               από τις τρείς πχ Ασθένεια.
        '''
        f = {'etyp': etyp, 'apod': apod, 'mtyp': mtyp[etyp]}
        # Ενημερώνουμε το f με τα ποσοστά ΙΚΑ και τις παρουσίες
        f['dpar'] = dpar
        f.update(dika)
        if etyp == MISTHOS: # , IMER, OROM
            f['misthos'] = dec(apod)
            f['imsthio'] = dec(dec(apod) / self.meres_mina_misthotoy)
            f['oromist'] = self.oromisthio(f['imsthio'])
        elif etyp == IMER:
            f['misthos'] = dec(dec(apod) * self.meres_mina_imeromisthioy)
            f['imsthio'] = dec(apod)
            f['oromist'] = self.oromisthio(f['imsthio'])
        elif etyp == OROM:
            f['oromist'] = dec(apod)
            f['imsthio'] = dec(f['oromist'] * self.ores_bdomadas / self.meres_bdomadas)
            f['misthos'] = dec(f['imsthio'] * self.meres_mina_imeromisthioy)
        else:
            f['misthos'] = 0
            f['imsthio'] = 0
            f['oromist'] = 0

        f['tot'] = {'ap_per': 0, 'ikaer': 0, 'ikaet': 0, 'ika': 0, 'ap_forol': 0}
        for par in f['dpar']:
            if par == 'dtac':
                self.calc_tac(f)
                f['tot']['ap_per'] += f['at']['ap_per']
                f['tot']['ikaer'] += f['at']['ikaer']
                f['tot']['ikaet'] += f['at']['ikaet']
                f['tot']['ika'] += f['at']['ika']
                f['tot']['ap_forol'] += f['at']['ap_forol']
            elif par == 'dype':
                self.calc_ype(f)
            elif par == 'dast':
                self.calc_astheneies(f)
                f['tot']['ap_per'] += f['aat']['ap_totf']
                f['tot']['ikaer'] += f['aat']['ikaer']
                f['tot']['ikaet'] += f['aat']['ikaet']
                f['tot']['ika'] += f['aat']['ika']
                f['tot']['ap_forol'] += f['aat']['ap_forol']
            else:
                # Υπάρχει λάθος στις παρουσίες
                pass
        foro, eea = self.calc_foro(f['tot']['ap_forol'])
        print(foro, eea)
        return f


def printm(f):
    t1 = u'{ap_per:>12} {ikaer:>12} {ikaet:>12} {ika:>11} {ap_forol:>12}\n'
    t2 = u'{dapo:<10} {deos:<10} {ap_per:>12} {ap_totf:>12} {ikaer:>12} {ikaet:>12} {ika:>11} {ap_forol:>12} {eas:>10} {isfas:>8}\n'
    t3 = u'{ap_per:>12} {ap_totf:>12} {ikaer:>12} {ikaet:>12} {ika:>11} {ap_forol:>12} {eas:>10} {isfas:>8}\n'
    tit = {'dapo': u'Από', 'deos': u'Έως', 'ap_per': u'Αποδοχές', 'ap_totf': u'Λ.Αποδοχ.',
           'ikaer': u'ΙΚΑ εργ.', 'ikaet': u'ΙΚΑ ετ.', 'ika': u'ΙΚΑ',
           'ap_forol': u'Καθαρά', 'eas': u'Επ.Ασθ.', 'isfas': u'Εισφ.Επιδ.'}
    tlin = "{0:-^120}\n".format('')
    tx = u'Αποτελέσματα Μισθοδοσίας\n'
    tx += u'Τύπος εργ   : %s\n' % f['mtyp']
    tx += u'Μισθός      : %s\n' % f['misthos']
    tx += u'Ημερομίσθιο : %s\n' % f['imsthio']
    tx += u'Ωρομίσθιο   : %s\n' % f['oromist']
    tx += tlin
    if 'at' in f:
        tx += u'Τακτικές αποδοχές περιόδου\n'
        tx += ' ' * 35 + t1.format(**f['at'])
        tx += tlin
    if 'aa' in f:
        tx += u'Αποδοχές ασθενείας περιόδου\n'
        tx += t2.format(**tit)
        for el in f['aa']:
            tx += t2.format(**el)
        tx += tlin
        tx += ' ' * 22 + t3.format(**f['aat'])
    tx += ' ' * 35 + t1.format(**f['tot'])
    return tx


if __name__ == '__main__':
    tst = Mis()
    # 'dtac': {'meres': xx, 'madeia': xx, 'onyxta': xx, 'oargia': xx, 'margia': xx}
    # 'dast': {'dapo': DDDD, 'deos': DDDD, 'masl3': xx, 'masm3': xx, 'mas0':xx, 'eas': xx }
    dst = [{'dapo': '2016-08-08', 'deos': '2016-08-10', 'masl3': 3},
           {'dapo': '2016-08-14', 'deos': '2016-08-19', 'masm3': 4, 'eas': 85},
           {'dapo': '2016-08-23', 'deos': '2016-08-31', 'masm3': 8, 'eas': 165},
           ]
    dst2 = {'dapo': '2016-08-14', 'deos': '2016-08-19', 'masl3': 3, 'masm3': 6, 'eas': 350},
    par = {'dtac': {'mergas': 16}, 'dast': dst}
    pika = {'pika':.4006, 'pikae': .155}
    print(printm(tst.calc1(MISTHOS, 2000, par, pika)))
    print(tst.calc1(MISTHOS, 2000, par, pika))
