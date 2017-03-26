# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from miles import frm_seq
from tables import tables


if __name__ == '__main__':
    from sys import argv, exit
    tbl = tables['eid']
    app = QtGui.QApplication(argv)

    form = frm_seq.Fsequencial(tables, 'inv', 1, invisible_fields=['id'])
    form.show()
    s = app.exec_()
    exit(s)
