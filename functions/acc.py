# -*- coding: utf-8 -*-
# Χειρισμος λογαριασμών λογιστικής
# Δημιουργία ανωτεροβαθμίων μέχρι το επίπεδο της ομάδας

from dec import dec
from file2txt import file2txt
from dec2str import dec2str
from date2str import date2str
from dbsqlite import Db


def isoz(accounts, diax='.'):
    '''
    [['20.00.00',0, 15], ['38.00.00', 34, 67]]
    '''
    dv = {}
    lena = len(accounts[0])
    for acc in accounts:
        ach = lmohier(acc[0], diax)  # ['2', '20', '20.00', '20.00.00']
        for el in ach:
            tlist = dv.get(el, [dec(0) for i in range(lena - 1)])
            for i, el2 in enumerate(acc[1:]):
                tlist[i] += dec(el2)
            dv[el] = tlist
    return dv


def lmohier(lmo, diax='.'):
    '''
    Επιστρέφει λίστα με την ιεραρχία του λογαριασμού
    πχ αν ο λογαριασμός είναι ο 38.00.00 επιστρέφει:
    ['total', '3', '38', '38.00', '38.00.00']
    '''
    hier = lmo.split(diax)
    flist = ['total', hier[0][0]]
    for i in range(len(hier)):
        flist.append(diax.join(hier[:i+1]))
    return flist


def dathier(dat):
    '''
    Επιστρέφει λίστα με την ιεραρχία ημερομηνίας
    π.χ αν ημερομηνία = 2016-10-28 επιστρέφει:
    ['2016', '2016-10', '2016-10-28']
    '''
    year, month, date = dat.split('-')
    return [year, '%s-%s' % (year, month), dat]


def isozpr(lmodic):
    '''
    Εκτύπωση ισοζυγίου λογαριασμών
    '''
    for key in sorted(lmodic.keys()):
        alist = lmodic[key]
        flist = []
        flist.append(key)
        for el in alist:
            flist.append(dec2str(el))
        # alist.insert(0, key)
        alen = len(alist)
        st = '{:16} '  + ('{:>16} ' * alen)
        print(st.format(*flist))


def tst():
    dapo = '2015-01-01'
    deos = '2015-12-31'
    sqlfile = './sql/selectp_isozygio1.sql'
    db = Db('/home/tedlaz/tedfiles/prj/samaras15/sam2015.sql3')
    sqlp = file2txt(sqlfile)
    sql = sqlp.format(apo=dapo, eos=deos)
    rws = db.rows(sql)
    isz = isoz(rws)
    print('Ισοζύγιο από %s έως %s' % (date2str(dapo), date2str(deos)))
    isozpr(isz)


if __name__ == '__main__':
    isz = isoz([['38.00.00', 10.22, 11.45, 0, 1],
                ['38.01.00', 2.36, 2.48, 1, 0],
                ['20.00.00', 34.45, 0, 0, 1],
                ['20.00.01', 22.45, 0, 0, 1],
                ['20.00.02', 34.89, 0, 0, 12.45],
                ['24.00.00', 1650.88, 0, 0, 13.76],
                ['24.00.01', 351.42, 0, 0, 0],
                ['40.00.02', 15, 0, 0, 0],
                ['40.00.00', 15, 0, 0, 0],
                ['40.00.01', 15, 0, 0, 0]
                ])
    isozpr(isz)
    print(dathier('2016-01-01'))
    # tst()
