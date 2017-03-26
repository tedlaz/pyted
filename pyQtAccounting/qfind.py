#!/usr/bin/env python
#coding=utf-8
'''
Created on 21 Φεβ 2011

@author: tedlaz
'''
import sys

from PyQt4 import QtGui, QtCore

import accounting as ac

class fFind(QtGui.QDialog):
    def __init__(self, args=None,parent=None,lmos='', per=''):
        super(fFind, self).__init__(parent)
        self.parent = parent
        if self.parent:
            self.db = self.parent.db
        else:
            self.db = 'ted.sql3'
        self.lmos = lmos
        self.per  = per
        self.table = QtGui.QTableWidget()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle(u"Αναζήτηση %s - %s" % (self.db, self.lmos))
        self.setMinimumSize(400, 500)
        self.populateTable()
        self.connect(self.table,QtCore.SIGNAL("cellDoubleClicked(int, int)"),self.sendVals)
        #self.connect(self.table,QtCore.SIGNAL("cellEntered(int,int)"),self.sendVals)
        self.a = ''
        self.b = ''
        
    def keyPressEvent(self,ev):
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            print 'ststa'
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self,ev)
        
    def val(self):
        return self.a
        
    def sendVals(self,x,y):
        self.a = self.table.item(x, 0).text()
        self.b = self.table.item(x, 1).text()
        self.accept()
        #self.close()
    
    def populateTable(self):
        self.table.setRowCount(0)
        lines = ac.findLmo(self.lmos, self.per, self.db)
        headers = [u'Λογαριασμός', u'Περιγραφή']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        for line in lines:
            self.setLine(line)
        self.table.resizeColumnsToContents()
        
    def setLine(self,item):
        rc = self.table.rowCount()
        self.table.setRowCount(rc+1)
        self.table.setItem(rc,0,strItem(item[0]))
        self.table.setItem(rc,1,strItem(item[1]))
        
def strItem(str):
    item = QtGui.QTableWidgetItem(str)
    return item

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = fFind(sys.argv,per = u'Π')
    form.show()
    sys.exit(app.exec_())            