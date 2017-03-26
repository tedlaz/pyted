# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pymiles import frm_master_detail
from tables import tables


if __name__ == '__main__':
    from sys import argv, exit
    tbl = tables['eid']
    app = QtGui.QApplication(argv)

    form = frm_master_detail.Fmaster_detail(tables,
                                            'inv',
                                            'invd',
                                            1
                                            )
    form.show()
    s = app.exec_()
    exit(s)
