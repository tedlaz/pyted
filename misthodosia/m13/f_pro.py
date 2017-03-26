# -*- coding: utf-8 -*-
'''
Created on 22 Ιαν 2013

@author: tedlaz
'''

from PyQt4 import QtGui, QtCore

from gui import ui_pro


class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        
        self.ui = ui_pro.Ui_Dialog()
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
        sql = "INSERT INTO m12_pro(prod,fpr_id,coy_id,eid_id,proy,aptyp_id,apod) VALUES('%s',%s,%s,%s,%s,%s,%s)"
        ar = []
        ar.append(self.ui.le_prod.text())
        ar.append(self.ui.le_fpr_id.text())
        ar.append(self.ui.le_coy_id.text())
        ar.append(self.ui.le_eid_id.text())
        ar.append(self.ui.le_proy.text())
        ar.append(self.ui.le_aptyp_id.text())
        ar.append(self.ui.le_apod.text())
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