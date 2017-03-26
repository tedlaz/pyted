#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import f2


# Λογαριασμός και υπόλοιπο που θα πρέπει πάντα να είναι θετικό
# ανάλογα φυσικά με την ομάδα του λογαριασμού
sql = '''select lmo.lmo, (sum(trd.pi) - sum(trd.xr))as vls
from trd
inner join lmo on lmo.id=trd.id_lmo
inner join tr on tr.id=trd.id_tr
WHERE tr.dat BETWEEN '{apo}' AND '{eos}'
AND substr(lmo.lmo, 1, 1) = '7'
group by lmo.lmo
UNION
select lmo.lmo, (sum(trd.xr) - sum(trd.pi))
from trd
inner join lmo on lmo.id=trd.id_lmo
inner join tr on tr.id=trd.id_tr
WHERE tr.dat BETWEEN '{apo}' AND '{eos}'
AND (substr(lmo.lmo, 1, 1) = '1' OR substr(lmo.lmo, 1, 1) = '2' OR substr(lmo.lmo, 1, 1) = '6')
group by lmo.lmo;
'''

#  Το υπόλοιπο ΦΠΑ της περιόδου
#  με εξαίρεση τις πληρωμές του ΦΠΑ (Λμος 54.00.9* κατά κανόνα)
sqlfpa = '''select (sum(trd.xr) - sum(trd.pi)) as vls
from trd
inner join lmo on lmo.id=trd.id_lmo
inner join tr on tr.id=trd.id_tr
WHERE tr.dat BETWEEN '{apo}' AND '{eos}'
AND (substr(lmo.lmo, 1, 7) BETWEEN '54.00.0' AND '54.00.8')
group by substr(lmo.lmo,1, 5);
'''

sqlfpa29 = '''select (sum(trd.xr) - sum(trd.pi)) as vls
from trd
inner join lmo on lmo.id=trd.id_lmo
inner join tr on tr.id=trd.id_tr
WHERE tr.dat BETWEEN '{apo}' AND '{eos}'
AND (substr(lmo.lmo, 1, 8) = '54.00.29')
group by substr(lmo.lmo,1, 5);
'''


def keyv():
    '''
    Συνάρτηση διαχείρησης εξαιρέσεων, για όσους λογαριασμούς δεν ακολουθούν
    κάποιο κανόνα συσχετισμού με λογαριασμούς ΦΠΑ.
    Στην τελική δομή οι εξαιρέσεις καταγράφονται σε αρχείο κειμένου ως εξής:
    24.02.00.000 353 303 341
    64.03.00 35723
    70.02.00.000 309 342
    '''
    f = {}
    f['24.02.00.000'] = [353, 303, 341]
    f['64.03.00'] = [35723,]
    f['70.02.00.000'] = [309, 342]
    return f


def readexeptions(fname):
    '''
    Συνάρτηση διαχείρησης εξαιρέσεων, για όσους λογαριασμούς δεν ακολουθούν
    κάποιο κανόνα συσχετισμού με λογαριασμούς ΦΠΑ.
    Οι εξαιρέσεις καταγράφονται σε αρχείο κειμένου (fname) ως εξής:
    Λογαριασμός  κ1    κ2  κ3  κλπ
    ------------ ---   --- --- ---
    24.02.00.000 353   303 341
    64.03.00     35723
    70.02.00.000 309 342
    Η συνάρτηση επιστρέφει dict : {}
    '''
    lins =''
    f = {}
    with open(fname) as fl:
        lins = fl.readlines()
    for lin in lins:
        if len(lin) < 6:  # αποκλείουμε γραμμές με μέγεθος < 6
            continue
        a = lin.split()
        key = a.pop(0)  # Το πρώτο στοιχείο είναι ο κωδικός
        f[key] = [int(i) for i in a]  # Τα υπόλοιπα είναι list of integers
    return f


def dicfromar(arr):
    '''
    Μετατρέπει ένα [[α1, β1], [α2, β2], ... [αν, βν]] σε
    {α1: β1, α2: β2, ... αν: βν}
    '''
    f = {}
    assert len(arr[0]) == 2
    for el in arr:
        f[el[0]] = f.get(el[0], f2.dec(0)) + f2.dec(el[1])
    return f


def getrows(db, tapo, teos):
    print('Φ2 για περίοδο από: %s  έως: %s' % (tapo, teos))
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(sql.format(apo=tapo, eos=teos))
    rws = cur.fetchall()

    cur.execute(sqlfpa.format(apo=tapo, eos=teos))
    fpa = f2.dec(cur.fetchone()[0])

    cur.execute(sqlfpa29.format(apo=tapo, eos=teos))
    fpa29 = f2.dec(cur.fetchone()[0])

    cur.close()
    con.close()

    # rowdic = makeit(dicfromar(rws), keyv())
    rowdic = makeit(dicfromar(rws), readexeptions('f2.exept'))
    rowdic[377] = fpa29
    if fpa > 0:
        rowdic[601] = fpa
    else:
        rowdic[611] = fpa * f2.dec(-1)

    return rowdic


def guess(lmo):
    '''
    Μαντεύει τον κωδικό του ΦΠΑ από το έντυπο Φ2 με δεδομένο ότι υπάρχει
    κάποια λογική αντιστοίχιση κατά τη δημιουργία των λογαριασμών
    Όποιος λογαριασμός δεν είναι προβλέψιμος μπαίνει σε συνάρτηση διαχείρησης
    εξαιρέσεων
    '''
    assert len(lmo) > 2
    cf = int(lmo[0])
    cl = int(lmo[-2:])
    g = {1: {0 : 35700, 11: 352, 13: 351, 16: 356, 23: 353, 24: 352},
         2: {0 : 35700, 11: 351, 13: 351, 16: 356, 23: 353, 24: 352},
         6: {0 : 35700, 11: 35713, 13: 35713, 23: 35723, 24: 35724},
         7: {0 : 309, 13: 301, 16: 306, 23: 303, 24: 302}
         }
    return g.get(cf, {}).get(cl, 0)

def makeit(k, f):
    vls = {}
    for key in k.keys():
        if  key in f.keys():  # if key then ok
           for kod in f[key]:
               vls[kod] = vls.get(kod, 0) + k[key]
        else:  # Here try to guess key ..
            vl = guess(key)
            vls[vl] = vls.get(vl, 0) + k[key]
    return vls


def txkey(dicti):
    final = {}
    for key in dicti.keys():
        tkey = 'i%s' % key
        final[tkey] = f2.grd(dicti[key])
    return final


if __name__ == '__main__':
    aa = f2.F2()
    vus = getrows('el2016.sql3', '2016-01-01', '2016-03-31')
    aa.calc(vus)
    html = ''
    with open('f2.html') as fl:
        html = fl.read()
    # print(aa)
    iv = txkey(aa.v)
    iv['etos'] = '2016'
    iv['tr'] = '2'
    iv['epon'] = 'Σαμαράς ΟΕ και δοκιμές'
    iv['onom'] = 'Tip'
    iv['patr'] = 'pater'
    iv['afm'] = '9999'
    iv['i400'] = ''
    # print(aa.v)
    with open('finaltst.html', 'w') as wfl:
        wfl.write(html.format(**iv))
    print(aa)
    print(guess('940.00.00.025'))
