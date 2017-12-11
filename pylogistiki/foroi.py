from utils import dec
from utils import dec2gr as d2g


class ForosException(Exception):
    pass


def foros_eisodimatos(xrisi, poso, paidia=0, misthotos=True):
    if int(xrisi) in (2016, 2017):
        result = foros_eis201617(poso, paidia, misthotos)
        result['xrisi'] = xrisi
        return result
    else:
        raise ForosException('Δεν υπάρχει συνάρτηση φόρου για το %s' % xrisi)


def foros_eis201617(poso, paidia, misthotos=True):
    '''
    Φόρος Έισοδήματος
    '''
    # foros = 0
    foros = dstr(poso, [20000, 10000, 10000], [22, 29, 37, 45])
    ekptosi_paidia = [1900, 1950, 2000, 2100]
    meiosi = 2100 if paidia > 3 else ekptosi_paidia[paidia]
    meiosi -= ((poso - 20000) / 1000.0 * 10.0) if poso > 20000 else 0
    meiosi = 0 if meiosi < 0 else meiosi
    meiosi = meiosi if misthotos else 0
    forosa = dec(0) if meiosi >= foros else foros - dec(meiosi)
    dic = {'forologiteo': dec(poso),
           'paidia': paidia,
           'typos': 'Μισθωτοί' if misthotos else 'Λοιποί',
           'forosKlimakas': foros,
           'meiosi': meiosi,
           'forosa': forosa,
           'forosp': forosa}
    if misthotos:
        pekptosis = dec(1.5)
        ekptosi = dec(forosa * pekptosis / dec(100))
        forosp = forosa - ekptosi
        dic['ekptosi'] = ekptosi
        dic['forosp'] = forosp
    eeakli = [12000, 8000, 10000, 10000, 25000, 135000]
    eeapos = [0, 2.2, 5, 6.5, 7.5, 9, 10]
    dic['eea'] = dstr(poso, eeakli, eeapos)
    dic['katharo'] = dic['forologiteo'] - dic['forosp'] - dic['eea']
    return dic


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


def dstr(poso, distribution=[100, 200, 700], perc=[0, 10, 30, 45]):
    '''
    distribution : [v1, v2, ...vn] -> [f1, f2, ..fn, fn+1]
    perc         : [p1, p2, ...pn, p(n+1)]
    Γίνεται μοίρασμα σε ποσά με βάση το distribution και το παραπάνω
    ποσό απο το vn γίνεται fn+1 και πάνω εκεί υπολογίζονται τα ποσοστά
    '''
    assert len(distribution) + 1 == len(perc)
    kat = []
    for el in distribution:
        if poso > el:
            kat.append(el)
            poso = poso - el
        else:
            kat.append(poso)
            poso = 0
            break
    # Εδώ βάζουμε το ποσό που έχει μένει υπόλοιπο
    if poso > 0:
        kat.append(poso)
    final = [kat[i] * perc[i] / 100.0 for i in range(len(kat))]
    # return kat, final, sum(kat), sum(final)
    return dec(sum(final))


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


def ek_ee(xrisi, poso, paidia=0, oldposo=0, oldprokataboli=0, tep=False):
    '''
    Εκκαθάριση Ελεύθερου επαγγελματία
    tep: Telos epitidefmatos
    '''
    if poso == 0:
        poso = dec(0.01)
    else:
        poso = dec(poso)
    if oldposo == 0:
        asfalisteo = poso
    else:
        asfalisteo = oldposo
    if tep:
        tel = dec(650)
    else:
        tel = dec(0)

    asfalisi = oaee_etisio(asfalisteo)
    katharo = poso - asfalisi
    foros = foros_eisodimatos(xrisi, float(katharo), paidia, False)
    prokataboli = foros
    eisfora = foros['eea']
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
    return log


def printfor(xrisi, poso_apo, poso_eos, bima=100, misthotos=True):
    '''
    Εκτύπωση πίνακα εισοδήματος και φόρων
    apo: Από εισόδημα
    eos: Έως εισόδημα
    bima: Βήμα ανάμεσα σε δύο γραμμές
    '''
    ast = "%12s %9s %9s %9s %9s %9s %9s"
    j = ('Εισόδημα', 'Φόρος 0', 'Φόρος 1', 'Φόρος 2', 'Φόρος 3', 'Ε.Ε.Αλ', 'f')
    print(ast % j)
    for i in range(poso_apo, poso_eos + bima, bima):
        print(ast % (d2g(i),
                     d2g(foros_eisodimatos(xrisi, i, 0, misthotos)['forosa']),
                     d2g(foros_eisodimatos(xrisi, i, 1, misthotos)['forosa']),
                     d2g(foros_eisodimatos(xrisi, i, 2, misthotos)['forosa']),
                     d2g(foros_eisodimatos(xrisi, i, 3, misthotos)['katharo']),
                     d2g(foros_eisodimatos(xrisi, i, 0, misthotos)['eea']),
                     d2g(foros_eisodimatos(xrisi, i, 3, misthotos)['ekptosi'])
                     ))
