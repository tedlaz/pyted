# -*- coding: utf-8 -*-
'''
Created on 22 Ιαν 2013

@author: tedlaz
'''

from PyQt4 import QtGui, QtCore, Qt

from gui import ui_pro
import qtutils

import widgets
class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None,tbl=None,titl=None,sql=None,headers=None,pardb=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.pardb = pardb
        self.ui = ui_pro.Ui_Dialog()
        self.ui.setupUi(self)
        self.makeConnections()
        
        if parent:
            self.db = parent.db
        else:
            self.db = 'c:/ted/mis.sql3'
        
        self.tbl = tbl    
        self.sql = sql
        self.headers = headers
        
        self.ui.t_tabl.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.t_tabl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.t_tabl.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.ui.t_tabl.setAlternatingRowColors(True)
        #self.table.setStyleSheet("alternate-background-color: yellow;background-color: rgba(180,180,180);")
        self.ui.t_tabl.setStyleSheet("alternate-background-color: rgba(213,251,227);")
        
        self.populate()
        self.setWindowTitle(titl)
        
    def populate(self):
        qtutils.populateTableWidget(self.ui.t_tabl, self.sql, self.headers, self.db) 
           
    def makeConnections(self):
        QtCore.QObject.connect(self.ui.b_newRec, QtCore.SIGNAL("clicked()"),self.newRecord)
        self.connect(self.ui.t_tabl,QtCore.SIGNAL("cellDoubleClicked(int,int)"),self.editRecord)
        self.ui.b_printPreview.clicked.connect(self.handlePreview)

    def newRecord(self):
        #form = f_generic_insert_update.dlg(parent=self,tbl=self.tbl,id=0)
        #form = f_master_detail.fmasterDetail(parent=self,tableName=self.tbl,id1=0,pardb=self.pardb)
        form = widgets.autoDialog(self.tbl,self.db,parent=self)
        if form.exec_() == QtGui.QDialog.Accepted:
            self.populate()
        
    def editRecord(self,x,y):
        idr = self.ui.t_tabl.item(x, 0).text()
        #form = f_generic_insert_update.dlg(parent=self,tbl=self.tbl,id=idr)
        #form = f_master_detail.fmasterDetail(parent=self,tableName=self.tbl,id1=idr,pardb=self.pardb)
        
        form = widgets.autoDialog(self.tbl,self.db,idr,parent=self)
        if form.exec_() == QtGui.QDialog.Accepted:
            self.populate()
            
    def handlePreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.ui.t_tabl.print_)
        dialog.exec_()
                     
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    title= u'Φυσικά πρόσωπα'
    sqla = 'select id , epon, onom,igen,pol,odo,num,tk from m12_fpr order by epon,onom'
    head = ['id',u'Επώνυμο',u'Όνομα',u'Ημ.Γέννησης',u'Πόλη',u'Οδός',u'Αριθμός',u'ΤΚ']
    form = dlg(sys.argv,tbl='m12_fpr',titl=title,sql=sqla,headers=head,pardb='../mispar.sql3')
    form.show()
    app.exec_()