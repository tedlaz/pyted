#!/usr/bin/python
# *- coding: utf-8 -*
import decimal
import sqlite3
import locale
import sys
import os
locale.setlocale(locale.LC_ALL, '')

if sys.version_info[0] > 2:
    python_v = 3
else:
    python_v = 2

cpath = os.path.dirname(os.path.abspath(__file__))


def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
        """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


def d2s(poso, decimals=2):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    def triades(txt, separator='.'):
        ltxt = len(txt)
        rem = ltxt % 3
        precSpace = 3 - rem
        stxt = ' ' * precSpace + txt
        a = []
        while len(stxt) > 0:
            a.append(stxt[:3])
            stxt = stxt[3:]
        a[0] = a[0].strip()
        fval = ''
        for el in a:
            fval += el + separator
        return fval[:-1]

    prosimo = ''
    strposo = str(poso)
    if len(strposo) > 0:
        if strposo[0] in '-':
            prosimo = '-'
            strposo = strposo[1:]
    val = dec(strposo, decimals)
    timi = '%s' % val
    if val == 0:
        prosimo = ''
    intpart, decpart = timi.split('.')
    final = triades(intpart) + ',' + decpart
    if final[0] == '.':
        final = final[1:]
    return prosimo + final


def getisoz(sqlis, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sqlis)
    rws = cur.fetchall()
    cur.close()
    con.close()
    dici = {}
    for el in rws:
        dici[el[0]] = el[1]
    for lmo in dici:
        if lmo[0] == '7':
            dici[lmo] = dici[lmo] * -1
    return dici


def get5400(sql54, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sql54)
    rws = cur.fetchall()
    cur.close()
    con.close()
    if rws:
        return dec(rws[0][0])
    else:
        return dec(0)


def guessf2(lmoi, dl2c, lg):
    # Λίστα λογαριασμών με τον αντίστοιχο κωδικό
    # Η λίστα αυτή είναι σε πρώτη επιλογή
    # Εάν δεν υπάρχει κάποιος λογαριασμός εδώ τότε προσπαθούμε να μαντέψουμε
    # τον κωδικό από το dictionary lg
    l2f = {}
    for lmo in lmoi:
        if lmo in dl2c:
            l2f[lmo] = dl2c[lmo]
        else:
            omada = lmo[0]
            fpa = lmo[-2:]
            l2f[lmo] = lg.get(omada, {}).get(fpa, 0)
    return l2f


def printDic(dic, title=''):
    print('')
    print(title)
    for el in sorted(dic):
        print('%s -> %s' % (el, dic[el]))
    print('')


def sumd(dic, sumkeys):
    val = dec(0)
    for key in sumkeys:
        val += dic.get(key, dec(0))
    return val


def f2n(isoz, dfpa5400, dl2c, lg, pisypol=0):
    # pf2 : Κωδικός εντύπου f2 για ποσά (πχ 361)
    # pf2i: Κωδικός εισόδου δεδομένων ανα συντελεστή φπα (πχ 36124))
    # vf2 : Κωδικός εντύπου f2 για φπα (πχ 381)

    # vf2v: Κωδικός υπολογιζόμενου φπα ανα συντελεστή (πχ 38124)
    v2fpa = {301: 331, 302: 332, 303: 333, 304: 334, 305: 335, 306: 336,
             361: 381, 362: 382, 363: 383, 364: 384, 365: 385, 366: 386}
    # κωδικοί ενδοκοινοτικών εισροών που μεταφέρονται αντίστοιχα σε εκροές
    eisSeEk = {36413: 30113, 36406: 30206, 36424: 30324, 36423: 30323,
               36409: 30409, 36404: 30504, 36417: 30617, 36416: 30616,
               36513: 30113, 36506: 30206, 36524: 30324, 36523: 30323,
               36509: 30409, 36504: 30504, 36517: 30617, 36516: 30616
               }
    dpf2i = guessf2(isoz.keys(), dl2c, lg)
    printDic(isoz, 'Ισοζύγιο')
    printDic(dpf2i, 'Αντιστοίχιση κωδικών')
    anafpa = {}
    # Αθροίζουμε απο το ισοζύγιο στους κωδικούς ανα λ/μο φπα
    for lmo in isoz:
        tlmo = dpf2i[lmo]
        anafpa[tlmo] = anafpa.get(tlmo, dec(0)) + dec(isoz[lmo])
        if tlmo in eisSeEk:
            elmo = eisSeEk[tlmo]
            anafpa[elmo] = anafpa.get(elmo, dec(0)) + dec(isoz[lmo])
    printDic(anafpa, 'Συνολα ανά λογαριασμό ΦΠΑ')
    f2i = {}
    for el in anafpa:
        sel = str(el)
        assert len(sel) == 5
        tpf2 = sel[:3]  # τα πρώτα ψηφία που αφορούν τον κωδικό
        pfpa = dec(dec(sel[3:]) / dec(100), 4)  # Τα τελευταία ψηφία του φπα

        pf2 = int(tpf2)
        # βρίσκουμε τον αντίστοιχο κωδικό εντύπου του φπα του αθροιστή
        lfpa = v2fpa.get(pf2, None)
        # Αθροίζουμε το ποσό στον βασικό αθροιστή
        f2i[pf2] = f2i.get(pf2, dec(0)) + anafpa[el]
        # Υπολογισμός φπα
        if lfpa:  # Εάν ο κωδικός έχει και φπα
            fpa = dec(anafpa[el] * pfpa)
            f2i[lfpa] = f2i.get(lfpa, dec(0)) + fpa
    # Εδώ κάνουμε αθροίσματα
    f2i[307] = sumd(f2i, range(301, 307))
    f2i[337] = sumd(f2i, range(331, 337))
    f2i[367] = sumd(f2i, range(361, 367))
    f2i[387] = sumd(f2i, range(381, 387))
    f2i[311] = sumd(f2i, [307, 342, 345, 348, 349, 310])
    f2i[312] = f2i[311] - sumd(f2i, [364, 365])
    # Ενημερώνουμε το πιστωτικό υπόλοιπο προηγούμενης περιόδου
    if pisypol > 0:
        f2i[401] = dec(pisypol)
    # Εδώ πρέπει να βάλω διαφορές φπα
    dfpa = f2i[337] - f2i[387]
    delta = dec(dfpa5400) - dfpa
    if delta < 0:
        f2i[402] = f2i.get(402, dec(0)) + dec(abs(delta))
    elif delta > 0:
        f2i[422] = dec(abs(delta))
    f2i[410] = sumd(f2i, [400, 402, 407])
    f2i[428] = sumd(f2i, [411, 422, 423])
    f2i[430] = f2i[387] + f2i[410] - f2i[428]
    ffpa = f2i[337] + f2i.get(483, dec(0)) - f2i[430]  # - f2i.get(401, dec(0))
    if ffpa < 0:
        f2i[470] = abs(ffpa)
        f2i[511] = dec(0)
        f2i[502] = f2i[470] + f2i.get(401, dec(0))
    else:
        f2i[480] = ffpa
        f2i[511] = ffpa - f2i.get(401, dec(0))
        f2i[502] = dec(0)
    printDic(f2i, 'Τελικό για f2')
    return f2i


def str_f2(f):
    for key in f:
        f[key] = locale.format("%0.2f", f[key], grouping=True)
    f[100] = ''
    k = {}
    for key in f:
        k['%s' % key] = f[key]
    st = ''
    st += '301:%(301)13s 331:%(331)12s 361:%(361)13s 381:%(381)12s\n'
    st += '302:%(302)13s 332:%(332)12s 362:%(362)13s 382:%(382)12s\n'
    st += '303:%(303)13s 333:%(333)12s 363:%(363)13s 383:%(383)12s\n'
    st += '304:%(304)13s 334:%(334)12s 364:%(364)13s 384:%(384)12s\n'
    st += '305:%(305)13s 335:%(335)12s 365:%(365)13s 375:%(385)12s\n'
    st += '306:%(306)13s 336:%(336)12s 366:%(366)13s 376:%(386)12s\n'
    st += '307:%(307)13s 337:%(337)12s 367:%(367)13s 377:%(387)12s\n'
    st += '342:%(342)13s\n'
    st += '345:%(345)13s               400:%(400)12s\n'
    st += '348:%(348)13s               402:%(402)12s 410:%(410)13s\n'
    st += '349:%(349)13s               407:%(407)12s\n'
    st += '310:%(310)13s\n'
    st += '311:%(311)13s               411:%(411)13s\n'
    st += '312:%(312)13s               422:%(422)12s 428:%(428)13s\n'
    st += '                            423:%(423)12s\n\n'
    st += '                            430:%(430)12s\n\n'
    st += '470:%(470)13s   480:%(480)13s\n\n'
    st += '401:%(401)13s   483:%(483)13s\n'
    st += '403:%(403)13s   505:%(505)13s\n'
    st += '404:%(404)13s\n'
    st += '502:%(502)13s   511:%(511)13s\n'
    st += '503:%(503)13s   523:%(523)13s\n'
    return st % k


def render_to_html(dat, pdata, filename):
    cd = [301, 302, 303, 304, 305, 306, 307,
          331, 332, 333, 334, 335, 336, 337,
          361, 362, 363, 364, 365, 366, 367,
          381, 382, 383, 384, 385, 386, 387,
          342, 345, 348, 349, 310, 311, 312,
          400, 402, 407, 410, 411, 422, 423, 428, 430,
          470, 401, 403, 404, 502, 503,
          480, 483, 505, 511, 523,
          507, 508,
          906, 907, 908]
    svl = ['apo', 'eos', 'epon', 'onom', 'patr', 'afm']
    with open(os.path.join(cpath, 'f2.html')) as html_template:
        if python_v == 2:
            html_text = html_template.read().decode('utf-8')
        else:
            html_text = html_template.read()
    fdict = {'i%s' % key: d2s(dat.get(key, '')) for key in cd}
    fdict.update({key: pdata.get(key, '') for key in svl})
    final = html_text.format(**fdict)
    with open(filename, 'w') as fout:
        if python_v == 2:
            fout.write(final.encode('utf-8'))
        else:
            fout.write(final)
