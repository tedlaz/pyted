# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from miles import frm_gridv
from tables import tables


if __name__ == '__main__':
    from sys import argv, exit
    tbl = tables['eid']
    app = QtGui.QApplication(argv)

    form = frm_gridv.Fgridv(tables,
                            'invd',
                            ftype='many',
                            invisible_fields=[]
                            )
    form.show()
    s = app.exec_()
    exit(s)
