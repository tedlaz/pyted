# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from miles import frm_grid
from tables import tables


if __name__ == '__main__':
    from sys import argv, exit
    tbl = tables['eid']
    app = QtGui.QApplication(argv)

    form = frm_grid.Fgrid(tables,
                          'pro',
                          ftype='many',
                          invisible_fields=[]
                          )
    form.show()
    s = app.exec_()
    exit(s)
