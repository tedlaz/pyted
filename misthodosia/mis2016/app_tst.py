# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pymiles.sqlite.db_meta import Metadb
from pymiles.gui.forms.tr_menu import Treemenu


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    app = QtGui.QApplication([])
    mv = QtGui.QDialog()
    mv.setWindowTitle(u'Πίνακες εφαρμογής')
    mv.meta = Metadb()
    mv.db = 'tst.sql3'
    trm = Treemenu(mv.meta.dic_for_menu(), mv)
    trm.setMinimumSize(260, 500)
    mv.setMinimumSize(260, 500)
    mv.show()
    s = app.exec_()
    sys.exit(s)
