# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

from PyQt4 import QtGui, QtCore, Qt
import dbutils as dbu
import qt_data_table_widget as dtw
import dbmodel as dbm

class fFind(QtGui.QDialog):
    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    '''
    def __init__(self, sql,db,tabl,canInsertNewRecord=1,parent=None):
        super(fFind, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        if db:
            self.lines, self.headers, status, mssg = dbu.dbRows(sql,db)
        
        self.sql = dbm.tblFlds(tabl) #sql
        self.db = db
        self.tbl= tabl
        self.canInsertNewRecord = canInsertNewRecord
        self.parent = parent
        self.colwidths = []     
        
        self.table = dtw.dataTableWidget(self.sql,self.tbl,self.db,self)

        layout = QtGui.QVBoxLayout()
                
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.setWindowTitle(dbm.getTableLabelPlural(self.tbl))
        self.setMinimumSize(500, 100)
        
        self.connect(self.table,QtCore.SIGNAL("cellDoubleClicked(int, int)"),self.sendVals)
        self.array = []
   
    def newRecord(self):
        self.table.newRecord()
              
    def keyPressEvent(self,ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self,ev)
        
    def val(self):
        return self.array
        
    def sendVals(self,x,y):
        for colu in range(self.table.columnCount()):
            self.array.append(self.table.item(x,colu).text())
        self.accept()
        
if __name__ == '__main__':
    pass