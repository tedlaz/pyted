# -*- coding: utf-8 -*-
'''
Created on 27 Μαρ 2013

@author: tedlaz
'''
from PyQt4 import QtGui,Qt
from utils import qtutils


class dlg(QtGui.QDialog):
    def __init__(self, sqlMaster,hMaster,sqlDetail,hDetail,title, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.sqlMaster = sqlMaster
        self.hMaster   = hMaster
        self.sqlDetail = sqlDetail
        self.hDetail   = hDetail
        
        if parent:
            self.db = parent.db
        else:
            self.db='c:/ted/dropbox/mis.sql3'
        
        self.tblMaster = QtGui.QTableWidget()
        self.tblMaster.setAlternatingRowColors(True)
        #self.tblMaster.setSortingEnabled(True)
        self.tblMaster.verticalHeader().setVisible(False)
        self.tblMaster.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblMaster.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self.tblDetail = QtGui.QTableWidget()
        self.tblDetail.setAlternatingRowColors(True)
        #self.tblDetail.setSortingEnabled(True)
        self.tblDetail.verticalHeader().setVisible(False)
        self.tblDetail.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblDetail.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        sp = QtGui.QSplitter(Qt.Qt.Vertical)
        sp.addWidget(self.tblMaster)
        sp.addWidget(self.tblDetail)
        
        layout = QtGui.QVBoxLayout()
        
        layout.addWidget(sp)
        
        self.setLayout(layout)
        
        self.populateMaster()               
        self.makeConnections()
        self.setWindowTitle(title)
        self.setMinimumSize(400, 300)
        
    def makeConnections(self):
        self.tblMaster.currentCellChanged.connect(self.populateDetail)
        
    def populateMaster(self):
        qtutils.populateTableWidget(self.tblMaster, self.sqlMaster, self.hMaster, self.db)
        
    def populateDetail(self,x,y,pre_x,pre_y):
        if x == pre_x:
            return
        sql = self.sqlDetail % self.tblMaster.item(x, 0).text()

        qtutils.populateTableWidget(self.tblDetail, sql, self.hDetail, self.db)

sqlMaster = '''
SELECT m12_par.id, m12_xrisi.xrisi, m12_period.periodp FROM m12_par
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_par.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_par.period_id
ORDER BY m12_xrisi.xrisi DESC, m12_period.id DESC
'''
hMaster = [u'id',u'Χρήση',u'Περίοδος']

sqlDetail = '''
SELECT m12_pard.id, m12_fpr.epon || ' ' || m12_fpr.onom AS onomatep,m12_ptyp.ptypp,pos 
FROM m12_pard
INNER JOIN m12_pro ON m12_pro.id=m12_pard.pro_id
INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_ptyp ON m12_ptyp.id=m12_pard.ptyp_id
WHERE par_id=%s
'''
hDetail = [u'id',u'Ονοματεπώνυμο',u'Τύπος',u'Ποσότης'] 
       
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sqlMaster,hMaster,sqlDetail,hDetail,u'Παρουσίες')
    form.show()
    app.exec_()