# -*- coding: utf-8 -*-
'''
Created on 22 Ιαν 2013

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore

from gui import ui_fpr


class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        
        self.ui = ui_fpr.Ui_Dialog()
        self.ui.setupUi(self)
        self.makeConnections()
        
        if parent:
            self.db = parent.db
        else:
            self.db = ''
        
    def makeConnections(self):
        QtCore.QObject.connect(self.ui.b_save, QtCore.SIGNAL("clicked()"),self.saveToDb)
    
    def saveToDb(self):
        from utils.dbutils import commitToDb
        sql = "INSERT INTO m12_fpr(epon,onom,patr,mitr,sex_id,igen,afm,amka,aika,pol,odo,num,tk) VALUES('%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s')"
        ar = []
        ar.append(self.ui.le_epon.text())
        ar.append(self.ui.le_onom.text())
        ar.append(self.ui.le_patr.text())
        ar.append(self.ui.le_mitr.text())
        ar.append(self.ui.le_sex.text())
        ar.append(self.ui.le_igen.text())
        ar.append(self.ui.le_afm.text())
        ar.append(self.ui.le_amka.text())
        ar.append(self.ui.le_aika.text())
        ar.append(self.ui.le_pol.text())
        ar.append(self.ui.le_odo.text())
        ar.append(self.ui.le_num.text())
        ar.append(self.ui.le_tk.text())
        if self.db:
            try:
                noId = commitToDb(sql % tuple(ar),self.db)
                QtGui.QMessageBox.warning(self,u'Επιτυχής αποθήκευση',u'Η εγγραφή αποθηκεύτηκε με αριθμό : %s' % noId) 
                #self.ui.le_id.setText(noId) 
            except Exception:
                QtGui.QMessageBox.warning(self,u'Λάθος κατά την αποθήκευση',u'Υπάρχει ήδη φυσικό πρόσωπο με αυτά τα στοιχεία')
        else:
            QtGui.QMessageBox.critical(self,u'Λάθος !!!',u'Δεν υπάρχει σύνδεση με Βάση Δεδομένων')   
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()