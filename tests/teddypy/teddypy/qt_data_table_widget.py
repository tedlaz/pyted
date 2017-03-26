# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

from PyQt4 import QtGui, QtCore

import utils
import qt_auto_form as aform
import dbutils as dbu
import dbmodel as dbm

tblStyle = "alternate-background-color: rgba(208,246,230);"

class sortWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, text, sortKey):
        #call custom constructor with UserType item type
        QtGui.QTableWidgetItem.__init__(self, text, QtGui.QTableWidgetItem.UserType)
        self.sortKey = sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey
    
class dataTableWidget(QtGui.QTableWidget):
    def __init__(self, sql, tbl=None,db=None, parent=None, lbls=None):
        super(dataTableWidget, self).__init__(parent)
        
        self.parent = parent
        self.sql    = sql
        self.tbl    = tbl
        self.db     = db
        self.headers= None
        self.lbls   = lbls 
        self.verticalHeader().setDefaultSectionSize(20)     #Εδώ ορίζουμε το πλάτος της γραμμής του grid
        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(False)
        
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)            
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        self.setAlternatingRowColors(True)
        self.setStyleSheet(tblStyle)  
        
        self.setToolTip(u'Με δεξί πλήκτρο ποντικιού μενού για \n Διόρθωση εγγραφής \n Νέα εγγραφή')
        self.setSortingEnabled(True) 
        self.populate()

    def _intItem(self,num):
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,QtCore.QVariant(num))
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return item
    
    def _numItem(self,num):
        item = sortWidgetItem(utils.strGrDec(num),num)
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return item
                    
    def _strItem(self,strv):
        st = '%s' % strv
        if st=='None' : st = ''
        item = QtGui.QTableWidgetItem(st)
        return item
    
    def _dateItem(self,strv):
        strv = '%s' % strv
        if len(strv) < 10:
            item = sortWidgetItem(strv,strv)
        else: 
            y,m,d = strv.split('-')
            item = sortWidgetItem('%s/%s/%s' % (d,m,y),strv)
        return item
    
    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        Action = menu.addAction(u"Διόρθωση Εγγραφής")
        Action.triggered.connect(self.openForEdit)
        Act2   = menu.addAction(u"Νέα εγγραφή")
        Act2.triggered.connect(self.newRecord)
        menu.exec_(event.globalPos())
        
    def openForEdit(self):
        frm = aform.autoForm(id=self.item(self.currentRow(),0).text(),tbl=self.tbl,db=self.db,parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            self.populate()
            
    def newRecord(self):
        frmnr = aform.autoForm(id=None,tbl=self.tbl,db=self.db,parent=self)
        if frmnr.exec_() == QtGui.QDialog.Accepted:
            self.populate()
                                         
    def populate(self):
        self.setRowCount(0)
        self.setSortingEnabled(False)
        lines, self.headers, status, mssg = dbu.dbRows(self.sql,self.db)
        columnTypes = []
        for el in self.headers:
            columnTypes.append(el[0])
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(dbm.getLabels(self.headers))
        for line in lines:
            rc = self.rowCount()
            self.setRowCount(rc+1)
            colNo = 0
            for col in line:
                if columnTypes[colNo] =='i': #Numeric values
                    self.setItem(rc,colNo,self._intItem(col))
                elif columnTypes[colNo] =='n':
                    self.setItem(rc,colNo,self._numItem(col))
                elif columnTypes[colNo] in 'de': #Date values
                    self.setItem(rc,colNo,self._dateItem(col))
                else: #Other values as text
                    self.setItem(rc,colNo,self._strItem(col))
                colNo += 1
        self.resizeColumnsToContents() 
        self.setSortingEnabled(True)
        #self.sortByColumn(0,0)

if __name__ == '__main__':
    pass