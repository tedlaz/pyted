# -*- coding: utf-8 -*-
name = 'pro'
namp = u'Προσλήψεις'
pname  = 'pro'
pnamp  = u'Εργαζόμενοι'

sql = u'''
SELECT m12_pro.id, m12_pro.prod, m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, m12_coy.coyp,m12_eid.eidp,m12_pro.proy, m12_aptyp.aptypp, m12_pro.apod, m12_apo.apold
FROM m12_pro
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_aptyp on m12_aptyp.id=m12_pro.aptyp_id
LEFT JOIN m12_apo on m12_apo.pro_id=m12_pro.id
ORDER BY prod DESC
'''
from PyQt4 import QtCore, QtGui, Qt

import utils_qt, utils_db
import report_table as tr

class dlg(QtGui.QWidget):
    def __init__(self,parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.parent = parent
        
        #Your gui here

        layout  = QtGui.QVBoxLayout()
        
        self.title = QtGui.QLabel(namp)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        #font.setItalic(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("color: rgb(0, 0, 127);")
        
        self.table = QtGui.QTableWidget()
        
        layout.addWidget(self.title)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
            
        self.sql = sql
        
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: rgba(213,251,227);")
        if self.parent:
            utils_qt.popTblWidget(self.table, self.sql,self.parent.db)
        #Connections Here
        self.table.cellDoubleClicked.connect(self._edit)
        
    def canAdd(self):
        return True
    
    def _add(self):
        import f_newEmployeeWizard
        wiz = f_newEmployeeWizard.NewEmpWizard(parent=self)   
        wiz.exec_()
        if self.parent:
            utils_qt.popTblWidget(self.table, self.sql,self.parent.db)
                           
    def canPrint(self):
        return True
    
    def _print(self):
        data = utils_db.getHeadersRows(sql,self.parent.db)
        f ={'orientation'  :1,  # 0:portait   1:landcape
            'pdfName'      :'pro.pdf',
            'fontFamily'   :'Helvetica',  
            'ReportHeader1':u'ΠΡΟΣΛΗΨΕΙΣ ΕΡΓΑΖΟΜΕΝΩΝ',
            'ReportHeader2':u'',
            'ReportHeader3':u'',
            'headerLabels':data[0],
            'columnSizes' :[3,10,20,10,20,10,10,7,10],
            'columnToSum' :[0,0,0,0,0,0,0,0,0], # 0: No Sum 1: Sum
            'columnTypes' :[0,3,0,0,1,0,0,2,3], # 0: text 1:integer 2:decimal 3:date 4:decimal one
            'columnAlign' :[0,1,0,0,0,1,0,2,1], # 0:left 1:center 2:right
            'footerLine'  :True,
            'footerText'  :u'This is a footer text for testing',
            'footerPageNumberText':u'Σελίδα',
            'data'        :list(data[1])
            }   
        rep = tr.qtTableReport(f)
        rep.printPreview()    
        
    def _edit(self,x,y):
        idr = self.table.item(x, 0).text()
        print 'test edit'
        '''
        form = widgets.autoDialog(self.tbl,self.db,idr,parent=self)
        if form.exec_() == QtGui.QDialog.Accepted:
            self.populate()
        '''        
#Automatic execution from Program        
def run(parent):
    #w = dlg(parent)
    parent.stackw.addWidget(dlg(parent))
    
def test():
    import sys
    app = QtGui.QApplication(sys.argv)
    myApp = dlg()
    myApp.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    test()    