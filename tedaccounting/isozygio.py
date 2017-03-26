# -*- coding: utf-8 -*-
# from sets import Set
import datetime
import decimal
import sqlite3
import os
from log_sxedio_gr import lm
from tedutil import dategr
from tedutil import dec


def select(dbpath, sql, version=None):
    """
    Connect to database and select records
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
        dat = dategr.group_selector(tr['dat'], per)
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


def isoz_list(db, sql, per='y'):
    tmpl1 = '%-14s %-45s'
    tmpl2 = '%14s'
    vals = select(db, sql)
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
            line.append(dec.dec(res[key].get(key2, 0)))
            # stf += tmpl2 % dec2gr(res[key].get(key2, 0))
        line.append(dec.dec(ttot[key]))
        # stf += tmpl2 % dec2gr(ttot[key])
        lines.append(line)
        # stf += '\n'
    return titles, lines

if __name__ == '__main__':
    dbpath = '/home/tedlaz/pyted/tedaccounting/tst.aba'
    # print(isoz_list(dbpath, sql, 'm6'))
    print(isoz_list(dbpath, 'SELECT * FROM vtr;', 'm6'))

