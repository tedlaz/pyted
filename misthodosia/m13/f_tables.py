# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui, QtSql,QtCore, Qt

from gui import ui_tables
from utils.dbutils import getDbRows

class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.ui = ui_tables.Ui_Dialog()
        self.ui.setupUi(self)
        
        # Εδώ γεμίζουμε to CBox με τα ονόματα των πινάκων
        prothema = 'm12_'
        arr = getDbRows("SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE '%s%%' ORDER BY name" % prothema,parent.db)
        for el in arr:
            self.ui.c_tables.addItem(el[0])
        
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(parent.db)
        self.db.open()
        
        self.model = QtSql.QSqlRelationalTableModel(self,self.db)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.setTable(arr[0][0])
        self.model.select()
        #self.view = self.ui.tb_table #QtGui.QTableView()
        self.ui.tb_table.setModel(self.model)

        self.makeConnections()
        
    def makeConnections(self):
        self.ui.c_tables.currentIndexChanged.connect(self.acceptt)
        self.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)
        
    def acceptt(self):
        a = self.ui.c_tables.currentText()
        self.model.setTable(a)
        self.model.select()
        
    def closeEvent(self,event):
        print 'This is closing'
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()