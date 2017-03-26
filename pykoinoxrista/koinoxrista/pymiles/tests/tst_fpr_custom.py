# -*- coding: utf-8 -*-
from PyQt4 import QtGui, Qt
from pymiles.sqlite.db_meta import Metadb
from pymiles.gui.forms.databind import Databind
from ui_fpr import Ui_Dialog


class Fpr(QtGui.QDialog, Ui_Dialog, Databind):

    def __init__(self, parent, table, id_=None):
        QtGui.QDialog.__init__(self, parent)
        Databind.__init__(self, parent, table, id_)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(400)
        self.setupUi(self)
        self.bsave.clicked.connect(self.save)
        for fld in self.meta.table_fields(self.table):
            self.qtfields[fld] = self.__getattribute__(fld)
        if id_:
            self.populate(id_)
        self.id.setVisible(False)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    par = QtGui.QDialog()
    par.meta = Metadb()
    par.db = 'tst.sql3'
    window = Fpr(par, 'fpr', 2)
    par.show()
    window.show()
    sys.exit(app.exec_())
