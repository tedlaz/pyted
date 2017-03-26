# -*- coding: utf-8 -*-
'''
Created on 20 Ιαν 2014

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore, Qt

import dbmodel as model
import qt_grids_report as rptt
import qt_data_table_widget as dtw 
       
class gridDlg(QtGui.QDialog):
    def __init__(self, tbl=None, db=None, parent=None):
        super(gridDlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.parent = parent
        self.db  = db
        
        self.val = tbl #dbu.getTblOrView(tbl,db)
        
        self.tbl = self.val
    
        self.sql = model.tblFlds(tbl)

        self.layout = QtGui.QVBoxLayout()

        self._makeTitle(model.getTableLabelPlural(self.val))
               
        self.table = dtw.dataTableWidget(self.sql,self.tbl,self.db,self)
        self.layout.addWidget(self.table)
        self.table.doubleClicked.connect(self.table.openForEdit)
        self.setLayout(self.layout)
        
    def _makeTitle(self,title):
        title = QtGui.QLabel(title)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setStyleSheet("color: rgb(0, 0, 127);")
        self.layout.addWidget(title)
        
    def newRecord(self):
        self.table.newRecord()
            
    def canAdd(self):
        return True
     
    def canPrint(self):
        return True
    
    def _print(self):
        frm = rptt.printGridForm(self.sql, self.tbl, self.db, self)
        frm.show()
           
class gridDlgMD(QtGui.QDialog): 
    def __init__(self, tbld=None,db=None,parent=None):
        super(gridDlgMD, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent
        self.db     = db
        
        tblm = tbld[:-1]

        self.tblMasterName = tblm
        self.sqlMaster = model.tblFlds(tblm)
        
        self.tblDetailName = tbld
        self.sqlDetail = model.tblFlds(tbld)
        
        self.layout = QtGui.QVBoxLayout()
        self.layoutd = QtGui.QVBoxLayout()
        
        splitter = QtGui.QSplitter()
        splitter.setOrientation(QtCore.Qt.Vertical)
        
        self.layout.addWidget(self._makeTitle(model.getTableLabelPlural(tblm) + ' > '+model.getTableLabelPlural(tbld) ))
            
               
        self.tblMaster = dtw.dataTableWidget(self.sqlMaster,self.tblMasterName,self.db,self)
        splitter.addWidget(self.tblMaster)
        self.tblDetail = dtw.dataTableWidget(self.sqlDetail,self.tblDetailName,self.db,self)
        splitter.addWidget(self.tblDetail)
        self.tblMaster.doubleClicked.connect(self.tblMaster.openForEdit)
        self.tblDetail.doubleClicked.connect(self.tblDetail.openForEdit)
        self.connect(self.tblMaster,QtCore.SIGNAL("currentCellChanged(int, int,int,int)"),self._updateDetail)
        self.layout.addWidget(splitter)
        self.setLayout(self.layout)
        
    def _updateDetail(self,x,y,a,b):
        conField = u''
        columnToHide = None
        for i,colName in enumerate(self.tblDetail.headers):
            if self.tblMasterName == colName[1:]:
                conField = colName
                columnToHide = i
                break 
        if self.tblMaster.item(x, 0):
            masterID = self.tblMaster.item(x, 0).text()
            self.tblDetail.sql = self.sqlDetail + u' WHERE %s=%s'% (conField,masterID) 
            self.tblDetail.populate()
            if columnToHide:
                self.tblDetail.hideColumn(columnToHide)
                    
    def _makeTitle(self,title):
        title = QtGui.QLabel(title)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setStyleSheet("color: rgb(0, 0, 127);")
        return title
    
    def canAdd(self):
        return False
    
    def canPrint(self):
        return False
    
def test():
    import sys
    import os
    import test_create_demo_db as tcd
    print(tcd.create_demo_db())
    app = QtGui.QApplication([])
    #dlg = masterDetailGridDlg('tstd', tcd.db)
    dlg = gridDlg('er', tcd.db)
    dlg.show()
    s = app.exec_()
    os.remove(tcd.db)
    sys.exit(s)
    
if __name__ == "__main__":
    test()