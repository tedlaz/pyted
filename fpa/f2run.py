# *- coding: utf-8 -*
import f2


def loadtmpl(afile):
    '''
    afile format:
    omada fpa kodikos (ο κωδικός μπορεί να είναι τριψήφιος ή πενταψήφιος)
    1 23 361
    2 00 36424
    ...
    '''
    lines = ''
    dic = {}
    with open(afile) as fl:
        lines = fl.readlines()
    for line in lines:
        if len(line) < 6:
            continue
        omada, fpa, kode = line.split()
        dic[omada] = dic.get(omada, {})
        if len(kode) == 3:
            dic[omada][fpa] = int(kode + fpa)
        elif len(kode) == 5:
            dic[omada][fpa] = int(kode)
    return dic


def loadsql(sqlfile):
    with open(sqlfile) as fl:
        return fl.read()


def loadacc(afile):
    '''
    afile format:
    logariasmos1 kodikos1
    logariasmos2 kodikos2
    ........
    '''
    lines = ''
    dic = {}
    with open(afile) as fl:
        lines = fl.readlines()
    for line in lines:
        if len(line) < 10:
            continue
        lmo, kode = line.split()
        dic[lmo] = int(kode)
    return dic


def checkDictionaries(tmplfile, lmoifile):
    tmpl = loadtmpl(tmplfile)
    for el in sorted(tmpl.keys()):
        print('{%s: %s}' % (el, tmpl[el]))
    lmoi = loadacc(lmoifile)
    print(lmoi)


def run(epon, apo, eos, db, htmlfile, tmplfile, lmoifile, sqlisf, sqlfpaf, pisyp=0):
    '''
    epon      : Επωνυμία εταιρείας
    apo       : Ημερομήνία iso από
    eos       : Ημερομηνία iso έως
    db        : Αρχείο βάσης δεδομένων sqlite
    htmlfile  : Το όνομα του αρχείου html για την αποθήκευση
    tmplfile  : Το όνομα του αρχείου txt που περιέχει τα guess templates
    lmoifile  : Το όνομα του αρχείου txt που περιέχει καρφωτά λογ/μους-κωδικούς
    sqlisf    : Το sql αρχείο που αφορά το ισοζύγιο
    sqlfpaf   : Το sql αρχείο που αφορά το υπόλοιπο ΦΠΑ
    pisyp     : Εάν υπάρχει το πιστωτικό υπόλοιπο προηγούμενης περιόδου
    '''
    #db = '/home/tedlaz/prj/samaras16b/el2016.sql3'

    pdata = {'apo': apo, 'eos': eos, 'epon': epon}
    sqlis = loadsql(sqlisf)
    sql54 = loadsql(sqlfpaf)
    isoz = f2.getisoz(sqlis.format(**pdata), db)
    ypfpa = f2.get5400(sql54.format(**pdata), db)
    pisyp = pisyp
    tmpl = loadtmpl(tmplfile)
    lmoi = loadacc(lmoifile)
    ap = f2.f2n(isoz, ypfpa, lmoi, tmpl, pisyp)

    f2.render_to_html(ap, pdata, htmlfile)
