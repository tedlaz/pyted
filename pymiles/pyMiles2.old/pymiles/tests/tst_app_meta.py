# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pymiles.sqlite.db_metaz import Metadbz
from pymiles.gui.forms.tr_menu import Treemenu


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    app = QtGui.QApplication([])
    mv = QtGui.QDialog()
    mv.setWindowTitle(u'Πίνακες meta')
    mv.meta = Metadbz()
    mv.db = 'app.meta'

    trm = Treemenu(mv.meta.dic_for_menu(), mv)
    mv.setMinimumSize(300, 300)
    mv.show()
    s = app.exec_()
    sys.exit(s)
