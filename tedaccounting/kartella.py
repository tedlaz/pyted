# -*- coding: utf-8 -*-
from tedutil import db
from tedutil.dec import dec
from tedqt import f_table


def kartella(lmos, dbf):
    sql = ("select id, dat, lmo, lmop, par, xr, pi "
           "from vtr "
           "where lmo like '%s%%' "
           "order by dat, lmo, id;") % lmos
    res = db.rowst(dbf, sql)
    rows = []
    tot = dec(0)
    for el in res:
        lin = [el[0], el[1], el[4], dec(el[5]), dec(el[6])]
        tot += dec(el[5]) - dec(el[6])
        lin.append(tot)
        rows.append(lin)
    lbls = [u'Νο', u'Ημ/νία', u'Παραστατικό', u'Χρέωση', u'Πίστωση',
            u'Υπόλοιπο']
    return rows, lbls

if __name__ == '__main__':
    dbf = '/home/tedlaz/tedfiles/prj/samaras16c/gl201609.sql3'
    ro, lb = kartella('38.00', dbf)
    import sys
    import PyQt5.QtWidgets as Qw
    app = Qw.QApplication([])
    dlg1 = f_table.Table_widget(lb, ro)
    dlg1.show()
    s = app.exec_()
    sys.exit(s)
