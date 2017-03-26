# -*- coding: utf-8 -*-
name = 'stam'
namp = u'Δοκιμή'
pname  = 'erg'
pnamp  = u'Εργαζόμενοι'

sql = u'''
SELECT m12_fpr.id,epon,onom,patr,mitr,sexp,igen,afm,amka,aika,pol,odo,num,tk 
FROM m12_fpr
INNER JOIN m12_sex ON m12_sex.id=m12_fpr.sex_id
'''

from PyQt4 import QtGui, Qt

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
        
    def canPrint(self):
        return True
    
    def canAdd(self):
        return False
    
    def _print(self):
        data = utils_db.getHeadersRows(sql,self.parent.db)
        f ={'orientation'  :1,  # 0:portait   1:landcape
            'pdfName'      :'fpr.pdf',
            'fontFamily'   :'Helvetica',  
            'ReportHeader1':u'ΣΤΟΙΧΕΙΑ ΕΡΓΑΖΟΜΕΝΩΝ',
            'ReportHeader2':u'',
            'ReportHeader3':u'',
            'headerLabels':data[0],
            'columnSizes' :[3,10,10,8,8,6,8,8,10,8,6,13,5,5],
            'columnToSum' :[0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 0: No Sum 1: Sum
            'columnTypes' :[0,0,0,0,0,0,3,0,0,0,0,0,0,0], # 0: text 1:integer 2:decimal 3:date 4:decimal one
            'columnAlign' :[0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 0:left 1:center 2:right
            'footerLine'  :True,
            'footerText'  :u'This is a footer text for testing',
            'footerPageNumberText':u'Σελίδα',
            'data'        :list(data[1])
            }   
        rep = tr.qtTableReport(f)
        rep.printPreview()

    def butpush(self):
        pass
        
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