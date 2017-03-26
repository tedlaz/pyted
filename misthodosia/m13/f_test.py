# -*- coding: utf-8 -*-
'''
Created on 24 Ιαν 2013

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore
from utils  import dbutils, qtutils
#import functools

def getFields(tableName,db):
    sql1 = "SELECT id, tname, tper FROM tbl WHERE tname='%s'" % tableName
    tname = dbutils.getDbOneRow(sql1,db)
    sql2 = "SELECT fname, fper, ftyp, frequired, fsql, ftitles FROM tbl_d WHERE tbl_id='%s'" % tname[0]
    ar   = dbutils.getDbRows(sql2, db)
    return tname, ar

class MyLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
            super(MyLineEdit, self).__init__(parent)
            self.notifiers = []
            self.iv        = 0
            self.firstFocus = False
            
    def register(self,obj,i):
        self.notifiers.append(obj)
        self.iv=i
        
    def updt(self):
        for el in self.notifiers:
            el.up(self)   

    def focusInEvent(self, event):
        self.firstFocus = not self.firstFocus
        if self.firstFocus:
            
            self.updt()
            
        #self.clearText()
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
            
class dlg(QtGui.QDialog):
    
    def __init__(self, args=None, parent=None, tbl='m12_pro'):
        super(dlg, self).__init__(parent)
        if parent:
            self.db = parent.db
        else:
            self.db = ''
            
        self.tbl = tbl
        self.tname, self.filds = getFields(self.tbl,'mispar.sql3')
        self.fldsNo = len(self.filds)
        insSql = "INSERT INTO %s (" % self.tname[1]
        tailSql = " VALUES ("
        updSql = "UPDATE %s SET " % self.tname[1]
        tailUpd = "WHERE id=%s" % 1
        self.labels = []
        self.flds   = []
        self.idvals = {}
        gridLayout = QtGui.QGridLayout()
        today = QtCore.QDate.currentDate()
        
        for i in range(self.fldsNo):
            self.labels.append(QtGui.QLabel(self.filds[i][1]))
            
            if self.filds[i][2] == 'text':
                self.flds.append(QtGui.QLineEdit())
                
            elif self.filds[i][2] == 'date':
                te = QtGui.QDateEdit()
                te.setCalendarPopup(True)
                te.setDate(today)
                self.flds.append(te)
                
            elif self.filds[i][2] == 'dec':
                #dsb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.flds.append(QtGui.QDoubleSpinBox())
                
            elif self.filds[i][2] == 'int':
                sb = QtGui.QSpinBox()
                sb.setMinimum(0)
                sb.setMaximum(2050)
                self.flds.append(sb)            
                
            elif self.filds[i][2] == 'fkey':
                self.idvals[self.filds[i][0]] = 0
                le = MyLineEdit() #QtGui.QLineEdit()
                #le.textEdited.connect(functools.partial(self.con,i))
                le.register(self,i)
                self.flds.append(le)
                
            else:
                self.flds.append(QtGui.QLineEdit())
                
            self.labels[i].setBuddy(self.flds[i])
            gridLayout.addWidget(self.labels[i],i,0)
            gridLayout.addWidget(self.flds[i],i,1)
            
            if i == (self.fldsNo-1):
                insSql += "%s)" % self.filds[i][0]
                tailSql += "'%s')"
                updSql += "%s=" % self.filds[i][0]
                updSql += "'%s' "
            else:
                insSql += "%s, " % self.filds[i][0]
                tailSql += "'%s',"
                updSql += "%s=" % self.filds[i][0]
                updSql += "'%s', "
                
        self.insertSql = insSql + tailSql
        print self.insertSql
        print updSql + tailUpd
        self.saveButton = QtGui.QPushButton(u'Αποθήκευση')
        gridLayout.addWidget(self.saveButton,self.fldsNo,0,self.fldsNo,-1)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(gridLayout)
        self.setLayout(layout)
        self.makeConnections()
        self.setWindowTitle(self.tname[2])
         
    def up(self,ob):

        self.con(ob.iv,1)
               
    def con(self,ii,val):
        sql = self.filds[ii][4]
        titles = self.filds[ii][5].split(' ')
        db = 'C:/ted/mis.sql3'
        a = qtutils.fFind(sql, titles, [10,300], db ,parent=self)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idvals[self.filds[ii][0]] = a.array[0]
            self.flds[ii].setText(a.array[1])
            
    def makeConnections(self):
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("clicked()"),self.saveToDb)

           
    def saveToDb(self):
        varr = []
        errors = 0
        errorLog = ''
        
        for i in range(self.fldsNo):
            
            if self.filds[i][2] == 'date':
                val = self.flds[i].date().toString('yyyy-MM-dd')
                
            elif self.filds[i][2] == 'fkey':
                val = self.idvals[self.filds[i][0]]
                if val == 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.labels[i].text()
                
            elif self.filds[i][2] == 'dec':
                val = self.flds[i].value()
                if val <= 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.labels[i].text()
                    
            elif self.filds[i][2] == 'int':
                val = self.flds[i].value()    
                            
            else:
                val = self.flds[i].text()
            
            if self.filds[i][3]:
                if len(str(val)) == 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.labels[i].text()

            varr.append(val)
            
        sqlinsert =  self.insertSql % tuple(varr)
        print sqlinsert
        if errors:
            QtGui.QMessageBox.warning(self,u'Προσοχή υπάρχουν λάθη',errorLog)
        else:
            if self.db:
                insNo = dbutils.commitToDb(sqlinsert, self.db)
                QtGui.QMessageBox.warning(self,u'Μια χαρά',u'Η εγγραφή αποθηκευτηκε με αριθμό : %s' % insNo)
            else:
                QtGui.QMessageBox.warning(self,u'Πρόβλημα',u'Δεν υπάρχει Βάση Δεδομένων')
                     
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()