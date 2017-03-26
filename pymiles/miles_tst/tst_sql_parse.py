# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from sys import argv, exit
from miles import u_db_sqlparse as sqp
from miles import tr_menu as trm


if __name__ == '__main__':
    db = 'tst.sql3'
    meta = sqp.return_meta(db)
    print(meta)
    vals = []
    for table in sorted(meta.keys()):
        f = {'name': table, 'title': table, 'typ': 'tbl'}
        vals.append(f)

    # vals = [{'name': 'erg', 'title': u'Εργαζόμενος', 'typ': 'tbl'},
    #         {'name': 'er2', 'title': u'Σκατά', 'typ': 'nbl'}]
    app = QtGui.QApplication(argv)

    form = trm.Treemenu(vals)
    form.show()
    s = app.exec_()
    exit(s)
