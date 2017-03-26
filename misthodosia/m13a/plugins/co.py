# -*- coding: utf-8 -*-
name = 'co'
namp = u'Στοιχεία επιχείρησης'
pname  = 'co'
pnamp  = u'Επιχείρηση'

sql = u'''
SELECT m12_co.id,cop,ono,pat,cotypp,ame,afm,doy,dra,pol,odo,num,tk,ikac,ikap 
FROM m12_co
INNER JOIN m12_cotyp ON m12_cotyp.id=m12_co.cotyp_id
'''

from PyQt4 import QtCore, QtGui, Qt
import utils_qt

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
        utils_qt.popTblWidget(self.table, self.sql,self.parent.db)
        #Connections Here
        #self.but.clicked.connect(self.butpush)
 
    def canAdd(self):
        return False
           
    def canPrint(self):
        return False
    
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