# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui,Qt
from utils import dbutils, widgets

isValSQL = '''
SELECT m12_par.id FROM m12_par
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_par.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_par.period_id
WHERE m12_xrisi.xrisi='%s' AND m12_period.period='%s'
'''
insParSQL = "INSERT INTO m12_par (xrisi_id, period_id) VALUES (%s, %s)"
insPardSQL= "INSERT INTO m12_pard (par_id, pro_id, ptyp_id, pos) VALUES (%s, %s, %s, %s)"

def automaticInsert(xrisi_id,period_id,db):
    from utils import variusSQL

    xrisi = dbutils.getDbSingleVal("SELECT xrisi FROM m12_xrisi WHERE id='%s'" % xrisi_id, db)
    period = dbutils.getDbSingleVal("SELECT period FROM m12_period WHERE id='%s'" % period_id, db)
    print xrisi_id, period_id
    
    par = dbutils.getDbOneRow(isValSQL %(xrisi,period), db)
    if par:
        print u'Έχουν γίνει εγγραφές για την περίοδο %s %s' % (xrisi,period)
        return False
    
    arr = dbutils.getDbRows(variusSQL.InsertParousiesSQL % (xrisi,period,xrisi,period), db)
    if not arr:
        print u'Δεν υπάρχουν εργαζόμενοι στην περίοδο %s %s' % (xrisi,period)
        return False
    for el in arr:
        for c in el:
            print c,
        print ''
    par_id = dbutils.commitToDb(insParSQL % (xrisi_id, period_id), db)
    insArr = []
    for el in arr:
        insArr.append(dbutils.commitToDb(insPardSQL % (par_id,el[0],1,0),db))
    print insArr
    
class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        if parent:
            self.db = parent.db
        else:
            self.db = None #'c:/ted/mis.sql3'

        xrisiLabel = QtGui.QLabel(u"Χρήση:")
        xrisi = widgets.DbComboBox(dbutils.getDbRows("SELECT id, xrisi FROM m12_xrisi", self.db))
        xrisiLabel.setBuddy(xrisi)
        
        perLabel = QtGui.QLabel(u"Περίοδος Παρουσιών:")
        per = widgets.DbComboBox(dbutils.getDbRows("SELECT id, periodp FROM m12_period", self.db))
        perLabel.setBuddy(per)       

        bcalc =  QtGui.QPushButton(u'Υπολογισμός')
        
        def calcmis():
            if not self.db:
                return
            xrid  = xrisi.getValue()
            perid = per.getValue()
            automaticInsert(xrid,perid, self.db)
            self.accept()
            
        bcalc.clicked.connect(calcmis)       
        glayout = QtGui.QGridLayout()
        
        glayout.addWidget(xrisiLabel,0,0)
        glayout.addWidget(xrisi,0,1)
 
        glayout.addWidget(perLabel,1,0)
        glayout.addWidget(per,1,1)
        
        vlayout = QtGui.QVBoxLayout()  
        vlayout.addLayout(glayout)
        vlayout.addWidget(bcalc) 
                    
        self.setLayout(vlayout)
        self.setWindowTitle(u'Αυτόματη εισαγωγή παρουσιών')
       
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()