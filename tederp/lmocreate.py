# *- coding: utf-8 -*
'''Functions to create accounts'''
from log_sxedio_gr import lm


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
            return '%s' % lm[code[:i + 1]]
    return ''


def mlmo(kode, fpa, xorid=0):
    '''
    ΔΗΜΙΟΥΡΓΙΑ ΚΙΝΟΥΜΕΝΟΥ ΛΟΓΑΡΙΑΣΜΟΥ ΚΑΙ ΠΕΡΙΓΡΑΦΗΣ
    ΛΛ.ΛΛ.00.ΧΦΦ
    ΛΛ.ΛΛ = ΔΕΥΤΕΡΟΒΑΘΜΙΟΣ ΛΟΓΙΣΤΙΚΗΣ
    X = (0 = εσωτερικό, 1 = Ενδοκοινοτικό, 2 = Εξωτερικό)
    ΦΦ = Συντελεστής ΦΠΑ
    πχ 70.00.00.024
    '''
    proel = '%s' % xorid
    xora = {0: u'εσωτερικού',
            1: u'ενδοκοινοτικές',
            2: u'εξωτερικού'}.get(xorid, 0)
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
    pfpa = ''
    if fpa > 0:
        pfpa = ' με ΦΠΑ %s%%' % fpa
    print(proel, kode)
    if (proel == '0') and (kode[0] == '6'):
        flmo = '%s%s' % (plmo, pfpa)
    else:
        flmo = '%s %s %s' % (plmo, xora, pfpa)
    '''
    ΔΗΜΙΟΥΡΓΙΑ ΚΙΝΟΥΜΕΝΟΥ ΛΟΓΑΡΙΑΣΜΟΥ ΦΠΑ ΚΑΙ ΠΕΡΙΓΡΑΦΗΣ
    54.00.ΛΛ.ΧΦΦ :
    ΛΛ = Πρωτοβάθμιος λογαριασμός,
    X = (0 = εσωτερικό, 1 = Ενδοκοινοτικό, 2 = Εξωτερικό)
    ΦΦ = Συντελεστής ΦΠΑ
    '''
    if fpa == 0:
        lfpa = cfpa = ''
    else:
        if kode[0] == '6':
            cfpa = 'ΦΠΑ Δαπανών %s%%' % fpa
            lfpa = '54.00.29.%s%s' % (proel, fpa)
        else:
            cfpa = 'ΦΠΑ γιά %s %s %s%%' % (findcode(kode), xora, fpa)
            lfpa = '54.00.%s.%s%s' % (kode[:2], proel, fpa)
    return clmo, flmo, lfpa, cfpa


def synlmo(catid, xorid=0):
    '''Creating account'''
    if catid == '26':
        tv1 = '30'
        tt1 = u'Πελάτες'
    elif catid == '7':
        tv1 = '50'
        tt1 = u'Προμηθευτές'
    else:
        tv1 = '99'
        tt1 = 'Λάθος catid'

    if xorid == 0:
        tv2 = '00'
        tt2 = u'εσωτερικού'
    elif xorid == 1:
        tv2 = '01'
        tt2 = u'ενδοκοινοτικοί'
    elif xorid == 2:
        tv2 = '02'
        tt2 = u'εξωτερικού'
    else:
        tv2 = '99'
        tt2 = u'Λάθος περιοχή συναλλασσόμενου'
    return '.'.join([tv1, tv2, '00']), ' '.join([tt1, tt2])


if __name__ == '__main__':
    print(mlmo('70.00', 13, 3))
    print(synlmo('7', 2))
