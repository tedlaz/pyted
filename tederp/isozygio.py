# -*- coding: utf-8 -*-
# from sets import Set
import datetime
import decimal
import sqlite3
import os
from log_sxedio_gr import lm


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimal digits
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
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


def dec2gr(poso, decimals=2, zeroAsSpace=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    if dec(poso) == dec(0):
        if zeroAsSpace:
            return ''
        else:
            decs = '0' * decimals
            if decimals > 0:
                return '0,' + decs
            else:
                return '0'

    def triades(txt, separator='.'):
        '''
        Help function to split digits to thousants ( 123456 becomes 123.456 )
        '''
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
    timi = '%s' % dec(strposo, decimals)
    intpart, decpart = timi.split('.')
    final = triades(intpart) + ',' + decpart
    if final[0] == '.':
        final = final[1:]
    return prosimo + final


def select(dbpath, sql, version=None):
    """

    """
    assert os.path.exists(dbpath)
    assert sql[:6].upper() == 'SELECT'
    con = sqlite3.connect(dbpath)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('PRAGMA user_version;')
    vfromdb = cur.fetchone()
    if version is not None:
        if version != vfromdb[0]:
            cur.close()
            con.close()
            print('Version not compatible')
            return None
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows


def getymd_from_iso(isodate):
    '''
    Year, month, date From isodate
    '''
    assert isodate[4] == '-'
    assert isodate[7] == '-'
    y, m, d = isodate.split('-')
    return int(y), int(m), int(d)


def saizon(dat, startmonth=10):
    '''
    Επιστρέφει ετήσιο διάστημα από μήνα
    dat : Ημερομηνία
    startmonth : Μήνας που αρχίζει η σαιζόν
    '''
    assert startmonth <= 12
    y, m, d = getymd_from_iso(dat)
    if m >= startmonth:
        return '%s-%s(%s)' % (y, y+1, startmonth)
    else:
        return '%s-%s(%s)' % (y-1, y, startmonth)


def week(dat):
    '''
    returns year-weekNumber
    '''
    y, m, d = getymd_from_iso(dat)
    wn = '%s' % datetime.date(y, m, d).isocalendar()[1]
    if len(wn) == 1:
        wn = '0' + wn
    return '%s-%s' % (y, wn)


def period(date, diast=2):
    '''
    επιστρέφει δίμηνο, τρίμηνο, τετράμηνο, εξάμηνο
    '''
    assert diast in (2, 3, 4, 6)
    dval = {2: u'οΔίμ', 3: u'οΤρίμ', 4: u'οΤετρ', 6: u'οΕξάμ'}
    year, month, date = getymd_from_iso(date)
    imonth = int(month)
    period = imonth // diast
    ypoloipo = imonth % diast
    if ypoloipo > 0:
        period += 1
    return '%s-%s%s' % (year, period, dval[diast])


def group_time_text(adate, per='m'):
    if per == 'd':  # Όλη η ημερομηνία
        dat = adate[:10]
    elif per == 'm':  # Έτος + μήνας ####-##
        dat = adate[:7]
    elif per == 'y':  # Έτος μόνο
        dat = adate[:4]
    elif per == 'm2':
        dat = period(adate, 2)
    elif per == 'm3':
        dat = period(adate, 3)
    elif per == 'm4':
        dat = period(adate, 4)
    elif per == 'm6':
        dat = period(adate, 6)
    elif per == 'w':
        dat = week(adate)
    elif per == 's':
        dat = saizon(adate)
    else:  # Default is Year
        dat = adate[:4]
    return dat


def lmo_hierarchy(lmos, split_char='.'):
    '''
    Δίνοντας ένα λογαριασμό της μορφής x2.34.56
    επιστρέφει ['x', 'x2', 'x2.34', 'x2.34.56', 't', <'t267' ή 't35'>]
    '''
    assert len(lmos) > 1
    listlmo = lmos.split(split_char)
    listfinal = ['t']
    if lmos[0] in '267':
        listfinal.append('t267')
    elif lmos[0] in '35':
        listfinal.append('t35')
    listfinal.append(lmos[0])
    tmp = ''
    for el in listlmo:
        if tmp == '':
            tmp = el
        else:
            tmp = split_char.join([tmp, el])
        listfinal.append(tmp)
    return listfinal


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


def group_by_time(data,  per='d', split_char='.'):
    '''
    Χρησιμοποιούμε όλα τα δεδομένα και τα μοιράζουμε σε δύο διαστάσεις
    στις γραμμές αθροίζουμε ιεραρχικά τα υπόλοιπα των λογαριασμών
    στις στήλες ορίζουμε τις χρονικές περιόδους (πχ δίμηνα ,τρίμηνα κλπ)
    Θα μπορούσαμε να κινηθούμε και ανάποδα και από τα δεδομένα αυτά να κάνουμε
    drill down και να φτάσουμε στα αρχικά αναλυτικά δεδομένα.
    '''
    totals = {}
    pers = set()
    lmop = {}
    ttot = {}
    tlines = {}
    for tr in data:
        dat = group_time_text(tr['dat'], per)
        pers.add(dat)
        lmohi = lmo_hierarchy(tr['lmo'], split_char)
        for lmo in lmohi:
            totals[lmo] = totals.get(lmo, {})
            totals[lmo][dat] = totals[lmo].get(dat, 0)
            try:
                totals[lmo][dat] += tr['xr'] - tr['pi']
            except TypeError:
                print('Error in line236 %s %s' % (tr['xr'], tr['pi']))
            # Δοκιμαστικό για να μαζέψω τις αντίστοιχες εγγραφές
            tlines[lmo] = tlines.get(lmo, {})
            tlines[lmo][dat] = tlines[lmo].get(dat, [])

            tlines[lmo][dat].append([tr['id'],
                                     tr['dat'],
                                     tr['par'],
                                     # tr['lmo'],
                                     # tr['lmop'],
                                     tr['xr'],
                                     tr['pi']
                                     ])
            # Στήλη με σύνολα γραμμών
            ttot[lmo] = ttot.get(lmo, 0) + tr['xr'] - tr['pi']
            # Δημιουργία περιγραφών λογαριασμών συνδυάζοντας τα δεδομένα
            # κινούμενων λογαριασμών με τα δεδομένα από το dictionary lm
            if lmo == tr['lmo']:
                lmop[lmo] = tr['lmop']
            else:
                lmop[lmo] = findcode(lmo)
    return totals, sorted(pers), lmop, ttot, tlines


def isoz_print(db, sql, per='y'):
    tmpl1 = '%-14s %-45s'
    tmpl2 = '%14s'
    vals = select(db, sql, 1963)
    res, pers, lmop, ttot, tlines = group_by_time(vals, per)
    stf = tmpl1 % (u'Λογαριασμός', u'Περιγραφή')
    for el in pers:
        stf += tmpl2 % el
    stf += tmpl2 % u'Σύνολο'
    stf += '\n'
    for key in sorted(res.keys()):
        stf += tmpl1 % (key, lmop[key])
        for key2 in pers:
            stf += tmpl2 % dec2gr(res[key].get(key2, 0))
        stf += tmpl2 % dec2gr(ttot[key])
        stf += '\n'
    print(stf)


def isoz_list(db, sql, per='y'):
    tmpl1 = '%-14s %-45s'
    tmpl2 = '%14s'
    vals = select(db, sql, 1963)
    res, pers, lmop, ttot, tlines = group_by_time(vals, per)

    titles = [u'Λογαριασμός', u'Περιγραφή']
    # stf = tmpl1 % (u'Λογαριασμός', u'Περιγραφή')
    for el in pers:
        titles.append(el)
        # stf += tmpl2 % el
    # stf += tmpl2 % u'Σύνολο'
    # stf += '\n'
    titles.append(u'Σύνολο')
    lines = []
    for key in sorted(res.keys()):
        line = [key, lmop[key]]
        # stf += tmpl1 % (key, lmop[key])
        for key2 in pers:
            line.append(dec(res[key].get(key2, 0)))
            # stf += tmpl2 % dec2gr(res[key].get(key2, 0))
        line.append(dec(ttot[key]))
        # stf += tmpl2 % dec2gr(ttot[key])
        lines.append(line)
        # stf += '\n'
    return titles, lines

if __name__ == '__main__':
    sql = ("select tr.id, tr.par, tr.dat, lmo.lmo, lmo.lmop, trd.xr, trd.pi "
           "From trd "
           "inner join lmo on trd.id_lmo=lmo.id "
           "inner join tr on tr.id=trd.id_tr ")
    # Με χρήση view
    sql1 = "select * from vtr_trd"
    dbpath = '/home/tedlaz/prj/samaras16c/gl201609.sql3'
    dbm = '/home/tedlaz/MEGAsync/gastst.sql3'
    kms = '/home/tedlaz/Downloads/kms/kms.sql3'
    # isoz_print('/home/tedlaz/prj/samaras16c/gl201609.sql3', sql, 'm2')
    il = isoz_list(kms, sql1, 'm2')
    print('\n'.join(map(str, il[1])))

    # print(diastim('2016-04-01', 6))
    # print(saizon('2016-04-01'))
    # print(lmo_hierarchy('71.00.00.023'))
