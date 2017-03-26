# -*- coding: utf-8 -*-
'''
Created on 24 Ιαν 2013

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore
import os
import dbutils, qtutils
#import functools
iconFind = os.path.join(os.path.dirname(__file__), 'icon_find.jpg')
iconSave = os.path.join(os.path.dirname(__file__), 'icon_save.jpg')

def getFields(tableName,db):
    sql1 = "SELECT id, tname, tper FROM tbl WHERE tname='%s'" % tableName
    tname = dbutils.getDbOneRow(sql1,db)
    sql2 = "SELECT fname, fper, ftyp, frequired, fsql, ftitles, sqlUpdate FROM tbl_d WHERE tbl_id='%s'" % tname[0]
    ar   = dbutils.getDbRows(sql2, db)
    return tname, ar

class ButtonLineEdit(QtGui.QLineEdit):
    buttonClicked = QtCore.pyqtSignal(bool)
    
    def __init__(self, icon_file=iconFind, parent=None):
        super(ButtonLineEdit, self).__init__(parent)
        self.notifiers = []
        self.iv        = 0
        self.firstFocus = False
        self.button = QtGui.QToolButton(self)
        self.button.setIcon(QtGui.QIcon(icon_file))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.focusInEvent)#self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),(self.rect().bottom() - buttonSize.height() + 1)/2)
        super(ButtonLineEdit, self).resizeEvent(event)
        
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
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
'''                            
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
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
 '''           
class dlg(QtGui.QDialog):
    
    def __init__(self, args=None, parent=None, tbl='m12_fpr', id=0):
        super(dlg, self).__init__(parent)
        
        self.id = int(id)
        
        if parent:
            self.db = parent.db
        else:
            self.db = 'c:/ted/mis.sql3'
            
        self.tbl = tbl
        
        self.tname, self.filds = getFields(self.tbl,'../mispar.sql3')
        
        self.fldsNo = len(self.filds)
        
        selSql = "SELECT "
        tailSel= "FROM %s WHERE id='%s'" % (self.tname[1],id)
        
        insSql = "INSERT INTO %s (" % self.tname[1]
        tailSql = " VALUES ("
        
        self.updSql = "UPDATE %s SET " % self.tname[1]
        self.tailUpd = "WHERE id=%s" 
                
        self.labels = []
        self.flds   = []
        self.idvals = {}
        gridLayout = QtGui.QGridLayout()
        today = QtCore.QDate.currentDate()
        
        
        
        idLabel = QtGui.QLabel('id')
        gridLayout.addWidget(idLabel,0,0)
        self.LineEditid = QtGui.QLineEdit()
        self.LineEditid.setEnabled(False)
        idLabel.setBuddy(self.LineEditid)
        gridLayout.addWidget(self.LineEditid,0,1)
        self.LineEditid.setText('%s' % self.id)
        
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
                self.flds.append(QtGui.QDoubleSpinBox())
                
            elif self.filds[i][2] == 'int':
                sb = QtGui.QSpinBox()
                sb.setMinimum(0)
                sb.setMaximum(2050)
                self.flds.append(sb)            
                
            elif self.filds[i][2] == 'fkey':
                self.idvals[self.filds[i][0]] = 0
                le = ButtonLineEdit() #MyLineEdit() #QtGui.QLineEdit()
                #le.textEdited.connect(functools.partial(self.con,i))
                le.register(self,i)
                le.setReadOnly(True)
                self.flds.append(le)
                
            else:
                self.flds.append(QtGui.QLineEdit())
                
            self.labels[i].setBuddy(self.flds[i])
            gridLayout.addWidget(self.labels[i],i+1,0)
            gridLayout.addWidget(self.flds[i],i+1,1)
            
            if i == (self.fldsNo-1):
                selSql += '%s ' % self.filds[i][0]
                insSql += "%s)" % self.filds[i][0]
                tailSql += "'%s')"
                self.updSql += "%s=" % self.filds[i][0]
                self.updSql += "'%s' "
            else:
                selSql += '%s, ' % self.filds[i][0]
                insSql += "%s, " % self.filds[i][0]
                tailSql += "'%s',"
                self.updSql += "%s=" % self.filds[i][0]
                self.updSql += "'%s', "
                
        self.selectSql = selSql + tailSel
        self.insertSql = insSql + tailSql   
          
        if self.id == 0:
            pass
        else:
            rowVal = dbutils.getDbOneRow(self.selectSql, self.db)
            if rowVal:
                for i in range(self.fldsNo):
                    
                    if self.filds[i][2] == 'date':
                        yr,mn,dt = rowVal[i].split('-')
                        qd = QtCore.QDate()
                        qd.setDate(int(yr),int(mn),int(dt))
                        self.flds[i].setDate(qd)
                        
                    elif self.filds[i][2] == 'dec':
                        self.flds[i].setValue(rowVal[i]) 
 
                    elif self.filds[i][2] == 'fkey':
                        self.idvals[self.filds[i][0]] = str(rowVal[i])
                        
                        if self.filds[i][6]:
                            sqlForField = self.filds[i][6] % rowVal[i]
                            sqlWhere = ''
                        else:
                            sqlForField = self.filds[i][4]
                            
                            if 'WHERE' in sqlForField:
                                sqlWhere = " AND id=%s" % rowVal[i]
                            else:
                                sqlWhere = " WHERE id=%s" % rowVal[i]
                        fkSql = sqlForField + sqlWhere
                        print fkSql
                        v = dbutils.getDbOneRow(fkSql, self.db)
                        self.flds[i].setText(v[1]) 

                    elif self.filds[i][2] == 'int':
                        self.flds[i].setValue(rowVal[i])
  
                    else:
                        self.flds[i].setText('%s' % rowVal[i])                           
               
            
        self.saveButton = QtGui.QPushButton(u'Αποθήκευση')
        self.saveButton.setIcon(QtGui.QIcon(iconSave))
        gridLayout.addWidget(self.saveButton,self.fldsNo+1,0,self.fldsNo+1,-1)
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
        a = qtutils.fFind(sql, titles, [10,300], self.db ,parent=self)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idvals[self.filds[ii][0]] = a.array[0]
            self.flds[ii].setText(a.array[1])
            
    def makeConnections(self):
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("clicked()"),self.saveToDb)

    def createSql(self):
        '''
        Να μεταφερθεί εδώ ο κώδικας που δημιουργεί sql
        '''
        pass
           
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
                if len('%s' % val) == 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.labels[i].text()

            varr.append(val)
            
        if self.id == 0:
            sqlToExecute = self.insertSql % tuple(varr)
        else:
            tail = self.tailUpd % self.id
            updateSql = self.updSql + tail
            sqlToExecute = updateSql % tuple(varr)
        #print 'sqlToExecute: %s' % sqlToExecute
        if errors:
            QtGui.QMessageBox.warning(self,u'Προσοχή υπάρχουν λάθη',errorLog)
        else:
            if self.db:
                insNo = dbutils.commitToDb(sqlToExecute, self.db)
                if insNo:
                    QtGui.QMessageBox.warning(self,u'Μια χαρά',u'Η εγγραφή αποθηκευτηκε με αριθμό : %s' % insNo)
                    self.id = insNo
                    self.LineEditid.setText('%s' % self.id)
                    self.accept()
                else:
                    QtGui.QMessageBox.warning(self,u'Μια χαρά',u'Η εγγραφή με αριθμό : %s Ενημερώθηκε' % self.id)
                    self.accept()
            else:
                QtGui.QMessageBox.warning(self,u'Πρόβλημα',u'Δεν υπάρχει Βάση Δεδομένων')
                     
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv,id=1 ,tbl='m12_pro')
    #print form.db
    form.show()
    app.exec_()