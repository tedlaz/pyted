# -*- coding: utf-8 -*-
'''
Created on 18 Φεβ 2011

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore
from ui_insertEggrafi import Ui_Dialog

import accounting as ac
import qfind as qf

class fInsertEggrafi(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(fInsertEggrafi, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.makeConnections()
        self.ui.tDetail.setColumnWidth(0,105)
        self.ui.tDetail.setColumnWidth(1,200)
        self.ui.tDetail.setColumnWidth(2,250)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.a = self.b = ''
        self.newLine()
        if parent:
            self.db = parent.db
        else:
            self.db = 'ted.sql3'

    def makeConnections(self):
        #QtCore.QObject.connect(self.ui.bNewLine,QtCore.SIGNAL("clicked()"), self.newLine)
        QtCore.QObject.connect(self.ui.bSave,QtCore.SIGNAL("clicked()"),self.saveToDB)
        self.connect(self.ui.tDetail,QtCore.SIGNAL("cellChanged(int, int)"),self.find) 
        self.connect(self.ui.tDetail,QtCore.SIGNAL("cellDoubleClicked(int, int)"),self.setFinalValue)
    def setFinalValue(self,x,y):  
        if y == 3:
            if not self.ui.tDetail.item(x,y) : self.ui.tDetail.setItem(x,y,QtGui.QTableWidgetItem('0'))
            self.ui.tDetail.setItem(x,y,QtGui.QTableWidgetItem('%s' % (ac.dec(self.ui.tDetail.item(x,y).text())+(self.ypol()*-1))))
        elif y == 4:
            if not self.ui.tDetail.item(x,y) : self.ui.tDetail.setItem(x,y,QtGui.QTableWidgetItem('0'))
            self.ui.tDetail.setItem(x,y,QtGui.QTableWidgetItem('%s' % (ac.dec(self.ui.tDetail.item(x,y).text())+self.ypol())))
                
    def keyPressEvent(self,ev):
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            if self.ui.tDetail.currentColumn() < self.ui.tDetail.columnCount()-1:
                self.ui.tDetail.setCurrentCell(self.ui.tDetail.currentRow(), self.ui.tDetail.currentColumn()+1)
            else:
                if (self.ui.tDetail.rowCount()-1) == self.ui.tDetail.currentRow():
                    if(self.ui.tDetail.item(self.ui.tDetail.currentRow(),0).text() == ''):
                        pass
                    else:
                        self.newLine()
                self.ui.tDetail.setCurrentCell(self.ui.tDetail.currentRow()+1, 0)
        QtGui.QDialog.keyPressEvent(self,ev) 
                     
    def find(self,x,y):
        #self.changed = not self.changed
        if y == 0:
            a = self.ui.tDetail.item(x, 0).text()

            if a <> self.a:
                
                #a = a[:-1]
                form = qf.fFind(parent=self, lmos= a)
                if form.exec_() == QtGui.QDialog.Accepted:
                    self.a = form.a
                    self.b = form.b
                    self.ui.tDetail.setItem(x,y,strItem(form.a))
                    self.ui.tDetail.setItem(x,y+1,strItem(form.b))
                    self.a = self.ui.tDetail.setItem(x,y,strItem(form.a))

        elif y == 1:
            b = self.ui.tDetail.item(x, 1).text()
            if b <> self.b:
                form = qf.fFind(parent=self, per=b)
                if form.exec_() == QtGui.QDialog.Accepted:
                    self.a = form.a
                    self.b = form.b
                    self.ui.tDetail.setItem(x,y-1,strItem(form.a))
                    self.ui.tDetail.setItem(x,y,strItem(form.b))
        elif y == 3 or y == 4:
            self.ui.txtYpol.setText('%s' % self.ypol())
            self.ui.tDetail.item(x,y).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    def ypol(self):
        ypol = ac.dec(0)
        xr = ac.dec(0)
        pi = ac.dec(0)
        rows = self.ui.tDetail.rowCount()
        for i in range(rows):
            if self.ui.tDetail.item(i,3):
                xr = ac.dec(self.ui.tDetail.item(i,3).text())
            else:
                xr = ac.dec(0)
            if self.ui.tDetail.item(i,4):
                pi = ac.dec(self.ui.tDetail.item(i,4).text())
            else:
                pi = ac.dec(0) 
            ypol = ypol + xr - pi
        return ypol
    def newLine(self):
        rc = self.ui.tDetail.rowCount()
        self.ui.tDetail.setRowCount(rc+1)
    def clearFields(self):
        self.ui.tParastatiko.setText('')
        #self.ui.tPerigrafi.setText('')
        for i in range(self.ui.tDetail.rowCount()):
            self.ui.tDetail.setItem(i,2,QtGui.QTableWidgetItem(''))
            self.ui.tDetail.setItem(i,3,QtGui.QTableWidgetItem(''))
            self.ui.tDetail.setItem(i,4,QtGui.QTableWidgetItem(''))
    def saveToDB(self):
        rows = self.ui.tDetail.rowCount()
        cols = self.ui.tDetail.columnCount()
        imnia = self.ui.dateEdit.date().toString('yyyy-MM-dd')
        par   = self.ui.tParastatiko.text()
        per   = self.ui.tPerigrafi.text()
        tran = ac.tran(imnia,par,per,self.db)
        for i in range(rows):
            ar = []
            for j in range(cols):
                if self.ui.tDetail.item(i,j) == None:
                    ar.append('')
                else:
                    ar.append(self.ui.tDetail.item(i,j).text())  
            tran.ln(ar[0],ar[3],ar[4],ar[2])
        if tran.isOk():
            a = tran.saveToDB()
            QtGui.QMessageBox.information(self, u"pyAccounting", u"Η εγγραφή αποθηκευτηκε με Νο: %s" % a)
            self.clearFields()
        else:
            QtGui.QMessageBox.information(self, u"pyAccounting", u"Δεν μπορεί να γίνει αποθήκευση") 
             
def strItem(str):
    item = QtGui.QTableWidgetItem(str)
    return item
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = fInsertEggrafi(sys.argv)
    form.show()
    app.exec_()
