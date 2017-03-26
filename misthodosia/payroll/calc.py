# -*- coding: utf-8 -*-

from collections import OrderedDict as od
from dec import dec


def mines_misthoton(xronia):
    '''
    Μήνες για αποζημίωση απόλυσης μισθωτών
    xronia : Χρόνια εργασίας στον εργοδότη
    '''
    # xronia must be integer
    xronia = int(xronia)
    mines = 0
    if xronia < 1:
        mines = 0
    elif xronia >= 1 and xronia < 4:
        mines = 2
    elif xronia >= 4 and xronia < 6:
        mines = 3
    elif xronia >= 6 and xronia < 8:
        mines = 4
    elif xronia >= 8 and xronia < 10:
        mines = 5
    elif xronia < 11:
        mines = 6
    elif xronia < 12:
        mines = 7
    elif xronia < 13:
        mines = 8
    elif xronia < 14:
        mines = 9
    elif xronia < 15:
        mines = 10
    elif xronia < 16:
        mines = 11
    elif xronia < 17:
        mines = 12
    elif xronia < 29:
        mines = 12 + (xronia % 17 + 1)
    else:
        mines = 24
    return mines


def meres_imeromisthion(xronia):
    '''
    Μέρες για αποζημίωση απόλυσης ημερομισθίων
    xronia : Χρόνια εργασίας στον εργοδότη
    '''
    meres = 0
    if xronia < 1:
        meres = 0
    elif xronia >= 1 and xronia < 2:
        meres = 7
    elif xronia >= 2 and xronia < 5:
        meres = 15
    elif xronia >= 5 and xronia < 10:
        meres = 30
    elif xronia >= 10 and xronia < 15:
        meres = 60
    elif xronia >= 15 and xronia < 20:
        meres = 100
    elif xronia >= 20 and xronia < 25:
        meres = 120
    elif xronia >= 25 and xronia < 30:
        meres = 145
    elif xronia >= 30:
        meres = 165
    return meres


def apoz_apol(xronia, apodoxes, misthotos=True, proeidopoiisi=False):
    '''
    Υπολογισμός αποζημίωσης απόλυσης
    '''
    if misthotos:
        apoz = apodoxes * 14.0 / 12.0 * mines_misthoton(xronia)
    else:
        apoz = apodoxes * 14.0 / 12.0 * meres_imeromisthion(xronia)
    if proeidopoiisi:
        apoz = apoz / 2
    return dec(apoz)


def doro_pasxa(meres, apodoxes, misthotos=True):
    '''
    meres για μισθωτούς οι ημερολογιακές μέρες εργασίας
          για ημερομίσθιους οι μέρες εργασίας.
    '''
    doro = 0
    if misthotos:
        if meres > 120:
            meres = 120
        doro = apodoxes * meres / 240.0 * 1.04166
    else:
        if meres > 97.5:
            meres = 97.5
        doro = apodoxes * meres / 6.5 * 1.04166
    return dec(doro)


def doro_xrist(meres, apodoxes, misthotos=True):
    '''
    meres για μισθωτούς οι ημερολογιακές μέρες εργασίας
          για ημερομίσθιους οι μέρες εργασίας.
    '''
    doro = 0
    if misthotos:
        if meres > 237.5:  # 25 * 19 / 2
            meres = 237.5
        doro = apodoxes * meres / 237.5 * 1.04166
    else:
        if meres > 200:
            meres = 200
        doro = apodoxes * meres / 8 * 1.04166
    return dec(doro)


def epidoma_adeias(meres, apodoxes, misthotos=True):
    epid = 0
    mep = 0
    if misthotos:
        mep = meres / 25.0 * 2.0
        if mep > 12.5:
            mep = 12.5
        epid = apodoxes * mep / 25.0
    else:
        mep = meres / 25.0 * 2.0
        if mep > 13:
            mep = 13
        epid = apodoxes * mep
    return dec(epid)


class Erg():
    '''
    Εργαζόμενος
    '''
    def __init__(self, apod,
                 pika=40.06,  # 45.66
                 pikae=15.5,  # 18.95
                 misth=True,
                 mam=25,
                 maw=6,
                 oaw=40):
        self.misthotos = misth
        self.apod = dec(apod)
        self.mam = dec(mam)  # Meres IKA ana mina (25)
        self.oaw = dec(oaw)  # Ores ana bdomada (40)
        self.maw = dec(maw)  # Meres IKA ana bdomada (6)
        self.pika = dec(pika)
        self.pikae = dec(pikae)

    def oromisthio(self):
        '''
        Ωρομίσθιο
        '''
        if self.misthotos:
            return dec(self.apod / self.mam * self.maw / self.oaw)
        else:
            return dec(self.apod * self.maw / self.oaw)

    def imeromisthio(self):
        '''
        Ημερομίσθιο
        '''
        if self.misthotos:
            return dec(self.apod / dec(25))
        else:
            return dec(self.apod)


class Parousies():
    '''
    Παρουσίες εργαζομένου
    '''

    def __init__(self, mpar,
                 mkar=0,
                 mkad=0,
                 oype=0,
                 onyx=0,
                 ale3=0,
                 amo3=0):
        self.mpar = dec(mpar)  # Κανονικές εργάσιμες
        self.mkar = dec(mkar)  # Κυριακές / Αργίες για προσάυξηση
        self.mkad = dec(mkad)  # Κανονική άδεια
        self.oype = dec(oype)  # Υπερωρίες ώρες
        self.onyx = dec(onyx)  # Ώρες νυχτερινής προσαύξησης
        self.ale3 = dec(ale3)  # Μέρες ασθένειας μικρότερες των τριών
        self.amo3 = dec(amo3)  # Μέρες ασθένειας μεγαλύτερες των τριών

    def meres(self):
        return self.mpar + self.mkad

    def calc(self, erg):
        pargia = dec(0.75)
        pnyxta = dec(0.25)
        ekato = dec(100)
        vl = od()
        vl['ar-par'] = '0000'
        vl['kad'] = '3612'
        vl['ama'] = '1884513'
        vl['amka'] = '12312312311'
        vl['epon'] = 'MAKRIS'
        vl['onom'] = 'George'
        vl['Patr'] = 'IOANNIS'
        vl['mitr'] = 'Georgia'
        vl['imgen'] = '10/02/1964'
        vl['AFM'] = '999888777'
        vl['PlirOrar'] = 0
        vl['olesErg'] = 0
        vl['kyriakes'] = dec(self.mkar, 0)
        vl['eid'] = '841020'
        vl['eldp'] = '00'
        vl['paketo'] = '0101'
        vl['pminas'] = '01'
        vl['petos'] = '2015'
        vl['apo'] = ''
        vl['eos'] = ''
        vl['ap_typ'] = '01'
        vl['meresAsf'] = dec(self.meres(), 0)
        if erg.misthotos:
            vl['imeromisthio'] = ''
        else:
            vl['imeromisthio'] = erg.apod
        if erg.misthotos:
            vl['apodn'] = dec(self.meres() / erg.mam * erg.apod)
        else:
            vl['apodn'] = dec(self.meres() * erg.apod)
        vl['apodargia'] = dec(erg.imeromisthio() * self.mkar * pargia)
        vl['nyxt'] = dec(erg.oromisthio() * self.onyx * pnyxta)
        vl['apod'] = vl['apodn'] + vl['apodargia'] + vl['nyxt']
        ika = dec(vl['apod'] * erg.pika / ekato)
        vl['ikae'] = dec(vl['apod'] * erg.pikae / ekato)
        vl['ikab'] = ika - vl['ikae']
        vl['ika'] = ika
        vl['epas'] = ''
        vl['eperg%'] = ''
        vl['eperg'] = ''
        vl['ikaeis'] = ika
        vl['plir'] = vl['apod'] - vl['ikae']
        return vl


def prncalc(dic):
    '''
    Pretty print dictionary
    '''
    for key in dic:
        print("%20s : %12s" % (key, dic[key]))


def foros_eis(poso, paidia=0, misthotos=False):
    '''
    Φόρος Έισοδήματος
    '''
    foros = 0
    if poso <= 20000:
        foros = poso * 0.22
    elif poso <= 30000:
        fprin = 20000 * 0.22
        foros = fprin + (poso - 20000) * 0.29
    elif poso <= 40000:
        fprin = (20000 * 0.22) + (10000 * 0.29)
        foros = fprin + (poso - 30000) * 0.37
    elif poso > 40000:
        fprin = (20000 * 0.22) + (10000 * 0.29) + (10000 * 0.37)
        foros = fprin + (poso - 40000) * 0.45

    if paidia == 0:
        meiosi = 1900
    elif paidia == 1:
        meiosi = 1950
    elif paidia == 2:
        meiosi = 2000
    else:
        meiosi = 2100

    if poso > 20000:
        meiosi -= (poso - 20000) / 1000.0 * 10.0

    if meiosi < 0:
        meiosi = 0

    if not misthotos:  # Den dikaioytai meiosi ...
        meiosi = 0

    if meiosi >= foros:
        return dec(0)
    else:
        return dec(foros - meiosi)


def foros_eispar(poso, paidia=0, misthotos=False, pekptosis=1.5):
    '''
    Φόρος εισοδήματος με έκπτωση παρακράτησης
    '''
    foros = foros_eis(poso, paidia, misthotos)
    ekptosi = dec(0)
    if misthotos:
        ekptosi = dec(foros * dec(pekptosis) / dec(100))
    return foros - ekptosi


def foros_ea(poso):
    '''
    Εισφορά Αλληλεγγύης
    '''
    foros = 0
    p20 = 8000 * 2.2 / 100.0
    p30 = p20 + 500  # (10000 * 5.0 / 100.0)
    p40 = p30 + 650  # (10000 * 6.5 / 100.0)
    p65 = p40 + 1875  # (25000 * 7.5 / 100.0)
    p22 = p65 + 13950  # (155000 * 9.0 / 100.0)
    if poso <= 12000:
        foros = 0
    elif poso <= 20000:
        foros = (poso - 12000) * 2.2 / 100.0
    elif poso <= 30000:
        foros = p20 + (poso - 20000) * 5.0 / 100.0
    elif poso <= 40000:
        foros = p30 + (poso - 30000) * 6.5 / 100.0
    elif poso <= 65000:
        foros = p40 + (poso - 40000) * 7.5 / 100.0
    elif poso <= 220000:
        foros = p65 + (poso - 65000) * 9.0 / 100.0
    else:
        foros = p22 + (poso - 220000) * 10.0 / 100.0
    return dec(foros)


def foros_ak(poso, xrisi=2016):
    '''
    Φόρος Ακίνητης περιουσίας (Ενοίκια)
    '''
    if xrisi == 2016:  # Εδώ να μπεί κώδικας για όλες τις χρήσεις
        pass
    foros = 0
    if poso <= 12000:
        foros = poso * 0.15
    elif poso <= 35000:
        foros = (12000 * 0.15) + (poso - 12000) * 0.35
    else:
        foros = (12000 * 0.15) + (23000 * 0.35) + (poso - 35000) * 0.45
    return dec(foros)


def oaee_etisio(poso, peis=26.95, min_mina=586.07):
    '''
    Υπολογισμός κρατήσεων πρώην ΟΑΕΕ, χωρίς επικουρικό.
    '''
    poso = dec(poso)
    peis = dec(peis)
    min_mina = dec(min_mina)
    min_etos = dec(min_mina * dec(12))
    max_etos = dec(min_mina * dec(12) * dec(10))
    log = u''
    log += u'Etisies apodoxes              : %12s\n' % dec(poso)
    if poso < min_etos:
        poso = min_etos
    if poso > max_etos:
        poso = max_etos
    log += u'Etisies apodoxes gia Asfalisi : %12s\n' % dec(poso)
    log += u'Apodoxes mina gia Asfalisi    : %12s\n' % dec(poso / dec(12.0))
    eis = dec(poso * peis / dec(100.0))
    log += u'Asfalistikes Eisfores         : %12s\n' % dec(eis)
    log += u'Priromi ana Dimino            : %12s\n' % dec(eis / dec(6.0))
    log += u'Pliromi ana Mina              : %12s\n' % dec(eis / dec(12.0))
    print(log)
    return dec(eis)


def ek_ee(poso, paidia=0, oldposo=0, oldprokataboli=0, tep=False):
    '''
    Εκκαθάριση Ελεύθερου επαγγελματία
    tep: Telos epitidefmatos
    '''
    if poso == 0:
        poso = dec(0.01)
    else:
        poso = dec(poso)
    if oldposo == 0:
        posoGiaAsfalisi = poso
    else:
        posoGiaAsfalisi = oldposo
    if tep:
        tel = dec(650)
    else:
        tel = dec(0)

    asfalisi = oaee_etisio(posoGiaAsfalisi)
    katharo = poso - asfalisi
    foros = foros_eis(float(katharo), paidia, False)
    prokataboli = foros
    eisfora = foros_ea(float(katharo))
    tcost = dec(asfalisi + foros + eisfora + tel)
    ptc = dec(tcost / dec(poso) * dec(100))
    ektam = dec(tcost + prokataboli - dec(oldprokataboli))
    pek = dec(ektam / dec(poso) * dec(100))
    katharo = dec(poso - tcost)
    pkath = dec(katharo / dec(poso) * dec(100))
    tsepi = dec(poso - ektam)
    pts = dec(tsepi / dec(poso) * dec(100))
    log = u''
    log += u'\n1.Εισόδημα      %12s\n' % dec(poso)
    log += u'\n2.Κόστος\n'
    log += u'  Ασφάλιση      %12s\n' % dec(asfalisi)
    log += u'  Φόρος εισοδ   %12s\n' % dec(foros)
    log += u'  Εισφορά       %12s\n' % eisfora
    log += u'  Τέλος επιτηδ. %12s\n' % tel
    log += u'  --------------------------\n'
    log += u'  Σύνολο φόρων  %12s (%s%%)\n' % (tcost, ptc)
    log += u'\n3.Ταμιακά\n'
    log += u'  Σύνολο φόρων  %12s\n' % tcost
    log += u'  Προκαταβολή   %12s\n' % prokataboli
    log += u'  Μείον προκαταβολή\n'
    log += u'  προηγ.έτους   %12s\n' % dec(oldprokataboli * -1)
    log += u'  --------------------------\n'
    log += u'  Εκταμίευση    %12s (%s%%)\n' % (ektam, pek)
    log += u'\n4.Καθαρό        %12s (%s%%)\n' % (katharo, pkath)
    log += u'\n5.Σε Τσέπη      %12s (%s%%)\n' % (tsepi, pts)
    print(log)


def printfor(apo, eos, bima=100, mis=False):
    '''
    Εκτύπωση πίνακα εισοδήματος και φόρων
    apo: Από εισόδημα
    eos: Έως εισόδημα
    bima: Βήμα ανάμεσα σε δύο γραμμές
    '''
    ast = "%12s %9s %9s %9s %9s %9s"
    j = ('Eisodima', 'foros 0', 'foros 1', 'foros 2', 'foros 3', 'Ep.All.')
    print(ast % j)
    if mis:
        fri = foros_eis  # par
    else:
        fri = foros_eis
    dea = foros_ea
    for i in range(apo, eos + bima, bima):
        print(ast % (i, fri(i, 0, mis), fri(i, 1, mis), fri(i, 2, mis), fri(i, 3, mis), dea(i)))
