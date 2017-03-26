# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pymiles.gui.fields.text_combo import Combo
from pymiles.sqlite.db_meta import Metadb

if __name__ == '__main__':
    import sys
    db = 'tst.sql3'
    app = QtGui.QApplication([])
    main = QtGui.QWidget()
    main.meta = Metadb()
    main.db = db
    dlg = Combo(main, 'eid_id', 3)
    main.show()
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
