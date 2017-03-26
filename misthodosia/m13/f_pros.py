# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore

from gui import ui_erg

class dlg(QtGui.QDialog):
    StyleSheet = """
QComboBox { color: darkblue; font-weight: bold; }
QLineEdit { color: darkgreen; font-weight: bold; }
QDateEdit { color: darkblue; }
QLineEdit[yellowback="true"] {
    background-color: rgb(255, 255, 127);
    color: darkblue;
}
"""

    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        
        self.ui = ui_erg.Ui_Dialog()
        self.ui.setupUi(self)
        self.makeConnections()
        if parent:
            self.db = parent.db
        else:
            self.db = ''
        self.setStyleSheet(dlg.StyleSheet)    
        self.ui.t_epon.setProperty("yellowback", QtCore.QVariant(True))
        self.testSql()
        
        
    def makeConnections(self):
        pass
    
    def testSql(self):
        if not self.db:
            return 
        import sqlite3
        sql = "SELECT * FROM m12_fpr"
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        a = cur.fetchone()
        cur.close()
        con.close()
        
        self.ui.t_epon.setText(a[1])
        self.ui.t_onom.setText(a[2])
        self.ui.t_pat.setText(a[3])
        self.ui.t_mit.setText(a[4])
        if a[5]:
            sex = u'Γυναίκα'
        else:
            sex = u'Άνδρας'
        self.ui.t_sex.setText(sex)    
            
        y,m,d = a[6].split('-')
        self.ui.d_gen.setDate(QtCore.QDate(int(y),int(m),int(d)))
        
        self.ui.t_afm.setText(a[7])
        self.ui.t_amka.setText(a[8])
        self.ui.t_amika.setText(a[9])
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()